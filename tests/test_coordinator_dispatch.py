# File: /trade-weaver/tests/test_coordinator_dispatch.py
import json

import pytest
from google.genai.types import Content, Part

from trade_weaver.sub_agents.market_analyst.schemas import MarketRegimeState

pytestmark = pytest.mark.asyncio


# @pytest.mark.xfail(
#     reason="This test is expected to fail until the agent is refactored."
# )
async def test_market_analyst_end_to_end_m2m_workflow(
    root_agent, adk_test_harness
):
    """
    Integration Test: Verifies the new M2M workflow for the market_analyst_agent.

    It validates:
    1.  The CoordinatorAgent accepts a JSON payload with params.
    2.  The market_analyst_agent pipeline runs successfully.
    3.  The CoordinatorAgent produces a final, consolidated JSON event.
    4.  The final event has a "status" of "success".
    5.  The final event's "result" field is a valid MarketRegimeState object.
    """
    runner, session_service = adk_test_harness
    session = await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="m2m_workflow_test",
    )

    # --- Input ---
    # This payload invokes the market_analyst_agent pipeline via the Coordinator.
    payload = {
        "target_agent": "market_analyst_agent",
        "parameters": {"exchange": "NASDAQ"},  # Pass 'exchange' as the parameter
    }
    content = Content(parts=[Part(text=json.dumps(payload))])

    # --- Execution ---
    # Collect all events from the generator
    events = [
        event
        async for event in runner.run_async(
            session_id=session.id, user_id="test_user", new_message=content
        )
    ]

    # --- FINAL EVENT VALIDATION ---
    assert events, "Test failed: No events were returned from the agent run."

    # 1. Get the very last event, which should be the Coordinator's final payload
    final_event = events[-1]
    assert (
        final_event.author == "trading_desk_coordinator"
    ), "The final event should be from the coordinator."
    assert (
        final_event.content and final_event.content.parts
    ), "The final event must have content."

    # 2. Parse the JSON content of the final event
    try:
        final_payload = json.loads(final_event.content.parts[0].text)
    except json.JSONDecodeError:
        pytest.fail(
            "The final event from the Coordinator was not valid JSON. "
            f"Content: {final_event.content.parts[0].text}"
        )

    # 3. Assert the status is 'success'
    assert (
        final_payload.get("status") == "success"
    ), f"The final status should be 'success'. Payload: {final_payload}"

    # 4. Assert the 'result' field exists and is a dictionary
    result_data = final_payload.get("result")
    assert isinstance(
        result_data, dict
    ), f"The 'result' field should be a dictionary. Payload: {final_payload}"

    # 5. Validate the result against the MarketRegimeState Pydantic schema
    try:
        MarketRegimeState(**result_data)
    except Exception as e:
        pytest.fail(
            "The 'result' field in the final payload is not a valid "
            f"MarketRegimeState object. Validation error: {e}. Payload: {final_payload}"
        )

    # 6. (Optional but good) Check a specific field to ensure data flowed correctly
    assert (
        result_data.get("exchange") == "NASDAQ"
    ), "The 'exchange' in the final result does not match the input parameter."
