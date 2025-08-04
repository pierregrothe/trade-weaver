# File: tests/test_analyzer_agent_workflow.py (Corrected)

import pytest
import os
from dotenv import load_dotenv

def load_environment():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(project_root, 'src', 'trade_weaver', '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
load_environment()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from trade_weaver.agents.analyzer_agent.agent import root_agent as analyzer_agent

@pytest.mark.asyncio
async def test_analyzer_agent_executes_universe_creation():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=analyzer_agent,
        app_name="trade-weaver-test",
        session_service=session_service
    )
    session = await session_service.create_session(
        app_name="trade-weaver-test", user_id="test_user", session_id="test_session"
    )
    user_message = Content(parts=[Part(text="Start the daily market analysis.")])
    tool_was_called = False
    final_response_text = ""

    async for event in runner.run_async(
        user_id=session.user_id, session_id=session.id, new_message=user_message
    ):
        if event.get_function_calls():
            if event.get_function_calls()[0].name == 'create_tradable_universe':
                tool_was_called = True
                print("INFO: Tool 'create_tradable_universe' was correctly called.")
        
        if event.is_final_response() and event.content and event.content.parts:
            text_content = event.content.parts[0].text
            if text_content:
                final_response_text = text_content.strip().lower()

    assert tool_was_called, "The agent should have called the 'create_tradable_universe' tool."
    # Check that some of our mock tickers are present in the final response.
    assert "aapl" in final_response_text and "tsla" in final_response_text, \
        f"The final response should contain the tickers from the tradable universe. Got: '{final_response_text}'"
    
    print(f"\nFinal agent response: '{final_response_text}'")
    print("\n✅ test_analyzer_agent_executes_universe_creation PASSED!")