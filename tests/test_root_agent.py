# File: /trade_weaver/tests/test_root_agent.py
"""
Robust unit tests for the deterministic root CoordinatorAgent.
These tests verify the agent's routing logic, error handling, and
correct interaction with sub-agents.
"""

import pytest
import json
from unittest.mock import MagicMock, AsyncMock

from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from trade_weaver import root_agent, CoordinatorAgent

# --- Unit Tests for the CoordinatorAgent ---

def test_root_agent_instantiation():
    """
    Unit Test: Checks that the root_agent is instantiated correctly.
    """
    assert isinstance(root_agent, CoordinatorAgent)
    assert isinstance(root_agent, BaseAgent)
    assert root_agent.name == "trading_desk_coordinator"
    assert not hasattr(root_agent, 'instruction')


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_str, expected_error_msg",
    [
        ("", "Error: No JSON payload provided."),
        ("{'invalid_json': True}", "Error: Invalid JSON payload."),
        ('{"parameters": {}}', "Error: 'target_agent' key missing from JSON payload."),
        ('{"target_agent": "non_existent_agent"}', "Error: Sub-agent 'non_existent_agent' not found."),
    ]
)
async def test_coordinator_agent_error_handling(
    payload_str, expected_error_msg
):
    """
    Unit Test: Verifies that the coordinator correctly handles various bad inputs.
    """
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name="test_app", session_service=session_service)
    await session_service.create_session(
        app_name="test_app", user_id="test_user", session_id="error_session"
    )
    
    content = Content(role="user", parts=[Part(text=payload_str)])

    # The agent should yield exactly one error event and then stop.
    events = [
        event async for event in runner.run_async(
            user_id="test_user", session_id="error_session", new_message=content
        )
    ]
    
    assert len(events) == 1, "Expected a single error event"
    final_response = events[0].content.parts[0].text
    assert expected_error_msg in final_response, "The error message did not match"

@pytest.mark.asyncio
async def test_coordinator_successful_delegation(mocker):
    """
    Unit Test: Verifies the coordinator correctly dispatches to a sub-agent
    and updates the session state.
    """
    # 1. Create a mock to represent our sub-agent.
    mock_sub_agent = MagicMock(spec=BaseAgent)
    mock_sub_agent.name = "pre_market_scanner_agent"
    
    async def mock_generator(*args, **kwargs):
        if False:
            yield
    mock_sub_agent.run_async = AsyncMock(side_effect=mock_generator)

    # 2. Patch the `find_sub_agent` method on the CoordinatorAgent CLASS.
    #    This ensures any instance created within this 'with' block will use our mock.
    mocker.patch.object(CoordinatorAgent, 'find_sub_agent', return_value=mock_sub_agent)

    # 3. Instantiate the REAL CoordinatorAgent. It will now have the patched method.
    test_coordinator = CoordinatorAgent(name="test_coordinator", sub_agents=[])

    # 4. Create the runner and session.
    session_service = InMemorySessionService()
    runner = Runner(agent=test_coordinator, app_name="test_app", session_service=session_service)
    await session_service.create_session(
        app_name="test_app", user_id="test_user", session_id="delegate_session"
    )

    # 5. Define the payload.
    payload = {
       "target_agent": "pre_market_scanner_agent",
       "parameters": { "exchange": "NASDAQ" }
    }
    query = json.dumps(payload)
    content = Content(role="user", parts=[Part(text=query)])

    # 6. Run the agent and exhaust the event stream.
    _ = [event async for event in runner.run_async(
        user_id="test_user", session_id="delegate_session", new_message=content
    )]

    # 7. Assert that our mock sub-agent's run method was called.
    mock_sub_agent.run_async.assert_awaited_once()

    # 8. Assert that the find_sub_agent method was called on the instance.
    test_coordinator.find_sub_agent.assert_called_once_with("pre_market_scanner_agent")

    # 9. Assert that the session state was correctly updated.
    updated_session = await session_service.get_session(
        app_name="test_app", user_id="test_user", session_id="delegate_session"
    )
    
    assert updated_session is not None
    assert updated_session.state.get("exchange") == "NASDAQ"