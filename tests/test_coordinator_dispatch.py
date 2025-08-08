# File: /trade-weaver/tests/integration/test_coordinator_dispatch.py

import pytest
import json
from google.genai.types import Content, Part
from trade_weaver.sub_agents.market_analyst.schemas import MarketRegimeState

pytestmark = pytest.mark.asyncio


@pytest.mark.xfail(
    reason="Known Issue: The current market_analyst_agent does not correctly manage state. "
    "This test defines the required end-to-end state transformations which the "
    "current agent fails to perform. The agent needs a full refactor to pass."
)
async def test_market_analyst_end_to_end_state_management(root_agent, adk_test_harness):
    """
    Integration Test: Verifies the full state lifecycle for the market_analyst_agent.
    This test serves as the acceptance criteria for the agent's functionality.

    It validates:
    1.  Initial state from the Coordinator is received.
    2.  Intermediate state from data-gathering tools is added.
    3.  Final structured state from the synthesizer is added and is valid.
    4.  The initial state is preserved throughout the run.
    """
    runner, session_service = adk_test_harness
    session = await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="integration_state_lifecycle",
    )

    # --- Input ---
    # The CoordinatorAgent will place 'market_proxy' into the initial state.
    payload = {
        "target_agent": "market_analyst_agent",
        "parameters": {"market_proxy": "QQQ"},
    }
    content = Content(parts=[Part(text=json.dumps(payload))])

    # --- Execution ---
    _ = [
        event
        async for event in runner.run_async(
            session_id=session.id, user_id="test_user", new_message=content
        )
    ]

    # --- DEEP STATE VALIDATION ---
    final_session = await session_service.get_session(
        app_name="test_app",
        user_id="test_user",
        session_id="integration_state_lifecycle",
    )
    final_state = final_session.state

    # 1. Verify PRESERVATION of initial state
    assert (
        final_state.get("market_proxy") == "QQQ"
    ), "State Assertion Failed: The initial 'market_proxy' parameter was lost."

    # 2. Verify AUGMENTATION by data-gathering tools
    assert (
        "vix_data" in final_state
    ), "State Assertion Failed: Missing 'vix_data' from gatherer."
    assert (
        "adx_data" in final_state
    ), "State Assertion Failed: Missing 'adx_data' from gatherer."
    assert isinstance(
        final_state.get("vix_data"), dict
    ), "'vix_data' should be a dictionary."

    # 3. Verify TRANSFORMATION by the synthesizer agent
    assert (
        "intermediate_market_regime" in final_state
    ), "State Assertion Failed: Missing 'intermediate_market_regime' from synthesizer."

    # 4. Verify VALIDITY of the final structured state
    try:
        # Pydantic will raise a ValidationError if the dictionary is not a valid
        # representation of the MarketRegimeState schema.
        MarketRegimeState(**final_state.get("intermediate_market_regime", {}))
    except Exception as e:
        pytest.fail(
            f"State Assertion Failed: The 'intermediate_market_regime' state "
            f"is not a valid MarketRegimeState object. Validation error: {e}"
        )
