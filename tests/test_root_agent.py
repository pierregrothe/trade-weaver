"""
Unit tests for the root CoordinatorAgent.
"""
import asyncio
import json
from unittest.mock import MagicMock, AsyncMock, patch

import pytest
from google.adk.agents import BaseAgent, InvocationContext
from trade_weaver.agent import CoordinatorAgent
from google.adk.events import Event
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Use pytest-asyncio for async tests
pytestmark = pytest.mark.asyncio

@patch("trade_weaver.agent.CoordinatorAgent.find_sub_agent")
async def test_coordinator_successful_delegation(mock_find_sub_agent):
    """
    Unit Test: Verifies the coordinator correctly dispatches to a sub-agent
    and updates the session state.
    """
    # --- 1. Mock Sub-Agent Setup (Corrected) ---

    # This is a helper function that IS an async generator.
    async def mock_sub_agent_run_async_generator(*args, **kwargs):
        # We can yield mock events here if we want to test that the
        # coordinator correctly streams them back. For this test,
        # an empty generator is sufficient.
        if False:
            yield

    # Create the mock for the sub-agent.
    mock_sub_agent = MagicMock(spec=BaseAgent)
    mock_sub_agent.name = "pre_market_scanner_agent"
    
    # CRITICAL FIX: The `run_async` attribute of the mock should not be an
    # AsyncMock. It should be a regular MagicMock whose return_value is
    # the async generator object itself.
    mock_sub_agent.run_async = MagicMock(
        return_value=mock_sub_agent_run_async_generator()
    )

    # Configure the patched find_sub_agent to return our mock.
    mock_find_sub_agent.return_value = mock_sub_agent

    # --- 2. Agent and Runner Setup ---
    # Instantiate the REAL CoordinatorAgent.
    test_coordinator = CoordinatorAgent(name="test_coordinator", sub_agents=[])

    session_service = InMemorySessionService()
    runner = Runner(agent=test_coordinator, app_name="test_app", session_service=session_service)
    await session_service.create_session(
        app_name="test_app", user_id="test_user", session_id="delegate_session"
    )

    # --- 3. Define the Payload and Run the Agent ---
    payload = {
       "target_agent": "pre_market_scanner_agent",
       "parameters": { "exchange": "NASDAQ" }
    }
    query = json.dumps(payload)
    content = Content(role="user", parts=[Part(text=query)])

    # Run the agent and exhaust the event stream.
    _ = [event async for event in runner.run_async(
        user_id="test_user", session_id="delegate_session", new_message=content
    )]

    # --- 4. Assertions ---
    # Assert that the coordinator found the correct sub-agent.
    mock_find_sub_agent.assert_called_once_with("pre_market_scanner_agent")

    # Assert that the sub-agent's run_async method was called exactly once.
    mock_sub_agent.run_async.assert_called_once()

    # Assert that the context passed to the sub-agent contains the correct state.
    call_args, _ = mock_sub_agent.run_async.call_args
    passed_context = call_args[0]
    assert isinstance(passed_context, InvocationContext)
    assert passed_context.session.state.get("exchange") == "NASDAQ"
    print("\nTest passed: Coordinator correctly updated state and delegated to the mocked sub-agent.")
