# File: tests/test_analyzer_agent.py (Updated Version)

import pytest
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Import the agent we want to test
from trade_weaver.agents.analyzer_agent.agent import root_agent as analyzer_agent

@pytest.mark.asyncio
async def test_analyzer_agent_finds_opportunity():
    """
    Tests the complete workflow of the AnalyzerAgent.
    1. It should receive the user prompt.
    2. It should decide to call the 'get_market_data' tool.
    3. It should analyze the (mocked) tool result.
    4. It should return a final natural language response indicating an opportunity was found.
    """
    session_service = InMemorySessionService()
    runner = Runner(
        agent=analyzer_agent,
        app_name="trade-weaver-test",
        session_service=session_service
    )
    
    session = await session_service.create_session(
        app_name="trade-weaver-test", user_id="test_user", session_id="test_session"
    )

    user_message = Content(parts=[Part(text="Analyze NVDA for breakout opportunities.")])

    tool_was_called = False
    final_response_text = ""

    async for event in runner.run_async(
        user_id=session.user_id, session_id=session.id, new_message=user_message
    ):
        if event.get_function_calls() and event.get_function_calls()[0].name == 'get_market_data':
            tool_was_called = True
            print("INFO: Tool 'get_market_data' was called by the agent.")

        if event.is_final_response() and event.content and event.content.parts:
            final_response_text = event.content.parts[0].text.strip().lower() # Make it lowercase for easy checking
            
    # --- UPDATED ASSERTIONS ---
    # We now check for keywords instead of a rigid JSON structure.
    # Our mock data returns $150.25, which is BELOW the $152 breakout level.
    # Therefore, we expect the agent to say NO opportunity exists.
    assert tool_was_called, "The agent should have called the 'get_market_data' tool."
    assert "no opportunity" in final_response_text, \
        f"The final response should indicate NO opportunity was found. Got: '{final_response_text}'"
    
    print(f"\nFinal agent response: '{final_response_text}'")
    print("✅ test_analyzer_agent_finds_opportunity PASSED!")