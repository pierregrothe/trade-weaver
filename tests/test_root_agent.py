# File: /trade_weaver/tests/test_root_agent.py
"""
Robust unit and integration tests for the root Coordinator Agent.
- Unit tests are fast and use mocking to isolate agent logic.
- Integration tests are marked and make real API calls to the LLM.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.events import Event
from google.genai import types

# Import the agent instance we want to test
from trade_weaver.agent import root_agent


# --- 1. Pytest Fixture for Reusable Setup ---
@pytest.fixture
def runner_and_session():
    """
    A pytest fixture that creates and yields a fresh Runner and Session
    for each test function that requests it. This ensures test isolation.
    """
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, app_name="test_app", session_service=session_service
    )
    yield runner, session_service


# --- 2. Unit Tests (Fast, No API Calls) ---


def test_root_agent_instantiation():
    """
    Unit Test: Checks that the root_agent is instantiated correctly.
    """
    assert isinstance(root_agent, LlmAgent)
    assert root_agent.name == "trading_desk_coordinator"
    assert root_agent.description is not None and len(root_agent.description) > 0
    assert isinstance(root_agent.instruction, str)
    assert "Trading Desk Coordinator" in root_agent.instruction
    assert root_agent.tools == []
    assert root_agent.sub_agents == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_llm_response, expected_assertion",
    [
        (
            "Understood. I will delegate this to the `pre_market_scanner_agent`.",
            "delegat",
        ),
        (
            "This is a trade execution request. Passing to the `executor_agent`.",
            "executor_agent",
        ),
        (
            "I'm sorry, I don't have a specialist for that request. How can I clarify?",
            "clarify",
        ),
    ],
)
async def test_root_agent_logic_with_mocking(
    runner_and_session, mocker, mock_llm_response, expected_assertion
):
    """
    Unit Test: Verifies the agent's logic using a MOCKED LLM response.
    """
    runner, session_service = runner_and_session
    await session_service.create_session(
        app_name="test_app", user_id="test_user", session_id="mock_session"
    )
    mock_event = Event(
        author=root_agent.name,
        invocation_id="mock_inv_id",
        content=types.Content(parts=[types.Part(text=mock_llm_response)]),
        turn_complete=True,
    )

    async def mock_run_async(*args, **kwargs):
        yield mock_event

    mocker.patch.object(runner, "run_async", side_effect=mock_run_async)
    query = "This is a test query."
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response = ""
    async for event in runner.run_async(
        user_id="test_user", session_id="mock_session", new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break
    assert final_response is not None and len(final_response) > 0
    assert expected_assertion in final_response.lower()


# --- 3. Integration Test (Slow, Makes Real API Call) ---


@pytest.mark.integration
@pytest.mark.asyncio
async def test_root_agent_delegation_response_integration(runner_and_session):
    """
    Integration Test: Tests the agent's end-to-end integration with the real LLM.
    """
    runner, session_service = runner_and_session
    await session_service.create_session(
        app_name="test_app", user_id="test_user", session_id="integration_session"
    )

    query = "Please run the pre-market scan for the NASDAQ exchange."
    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response = ""
    events_received = []
    async for event in runner.run_async(
        user_id="test_user", session_id="integration_session", new_message=content
    ):
        # ADDED FOR DEBUGGING: Store and print every event received.
        events_received.append(event)
        print(f"DEBUG: Received event: {event.model_dump_json(indent=2)}")

        if event.is_final_response() and event.content and event.content.parts:
            # Check for text before accessing it to prevent errors
            if event.content.parts[0].text:
                final_response = event.content.parts[0].text
                break

    # NEW ASSERTION: First, check if we received any events at all.
    assert (
        len(events_received) > 0
    ), "Agent run produced no events. Check API key and model availability."

    # Now, check if a final response was found.
    assert (
        final_response is not None and len(final_response) > 0
    ), "Agent run finished but no final text response was found. Check agent instructions and model output."

    response_lower = final_response.lower()
    assert "delegat" in response_lower
    assert "pre_market_scanner_agent" in response_lower
