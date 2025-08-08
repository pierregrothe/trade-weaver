# File: /trade-weaver/tests/unit/test_coordinator_agent.py

import pytest
import json
from unittest.mock import MagicMock, patch
from google.adk.agents import BaseAgent, InvocationContext
from google.genai.types import Content, Part

pytestmark = pytest.mark.asyncio


# Helper to correctly mock an agent's async generator `run_async` method
async def mock_sub_agent_run_generator(*args, **kwargs):
    if False:
        yield


@patch("trade_weaver.agent.CoordinatorAgent.find_sub_agent")
async def test_coordinator_correctly_sets_initial_state_for_sub_agent(
    mock_find_sub_agent, adk_test_harness
):
    """
    Unit Test: Verifies the coordinator's primary state management duty:
    to correctly populate the session state from the payload's 'parameters'
    before delegating control.
    """
    runner, session_service = adk_test_harness
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user", session_id="unit_state_init"
    )

    # Setup Mock
    mock_sub_agent = MagicMock(spec=BaseAgent)
    mock_sub_agent.name = "market_analyst_agent"
    mock_sub_agent.run_async.return_value = mock_sub_agent_run_generator()
    mock_find_sub_agent.return_value = mock_sub_agent

    # Define Payload and Run
    payload = {
        "target_agent": "market_analyst_agent",
        "parameters": {"exchange": "NASDAQ", "user_level": "pro"},
    }
    content = Content(role="user", parts=[Part(text=json.dumps(payload))])
    _ = [
        event
        async for event in runner.run_async(
            session_id=session.id, user_id="test_user", new_message=content
        )
    ]

    # Assertions
    mock_find_sub_agent.assert_called_once_with("market_analyst_agent")
    mock_sub_agent.run_async.assert_called_once()

    # **CRITICAL STATE ASSERTION**: Verify the coordinator correctly passed the
    # 'parameters' from the payload into the session state for the sub-agent.
    passed_context = mock_sub_agent.run_async.call_args[0][0]
    assert isinstance(passed_context, InvocationContext)
    assert (
        passed_context.session.state.get("exchange") == "NASDAQ"
    ), "Coordinator failed to set the 'exchange' parameter in the state."
    assert (
        passed_context.session.state.get("user_level") == "pro"
    ), "Coordinator failed to set the 'user_level' parameter in the state."


# The parameterized error test remains the same.
@pytest.mark.parametrize(
    "test_id, payload_str, expected_error_fragment",
    [
        ("invalid_json", "this is not valid json", "Invalid JSON payload."),
        (
            "missing_key",
            json.dumps({"parameters": {}}),
            "'target_agent' key missing",
        ),
        (
            "agent_not_found",
            json.dumps({"target_agent": "non_existent_agent"}),
            "Sub-agent 'non_existent_agent' not found.",
        ),
        ("no_payload", "", "No JSON payload provided."),
    ],
)
async def test_coordinator_error_conditions(
    test_id, payload_str, expected_error_fragment, root_agent, adk_test_harness
):
    """
    Unit Test: Verifies the coordinator returns a structured JSON error event
    under various failure conditions.
    """
    runner, session_service = adk_test_harness
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user", session_id=test_id
    )
    content = Content(parts=[Part(text=payload_str)])

    # --- Execution ---
    events = [
        event
        async for event in runner.run_async(
            session_id=session.id, user_id="test_user", new_message=content
        )
    ]

    # --- Assertions ---
    assert len(events) == 1, "Expected exactly one error event."
    final_event = events[0]
    assert final_event.author == root_agent.name

    # 1. Assert the event content is valid JSON
    try:
        error_payload = json.loads(final_event.content.parts[0].text)
    except (json.JSONDecodeError, IndexError):
        pytest.fail("The error event content was not valid JSON.")

    # 2. Assert the JSON payload has the correct error structure
    assert error_payload.get("status") == "error"
    assert "result" in error_payload, "Error payload must have a 'result' field."
    assert (
        "error_message" in error_payload["result"]
    ), "Error result must have an 'error_message' key."

    # 3. Assert the specific error message is present
    assert (
        expected_error_fragment in error_payload["result"]["error_message"]
    ), "The expected error message was not found in the payload."
