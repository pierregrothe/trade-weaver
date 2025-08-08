"""
Unit tests for the Market Analyst Agent.

This test suite validates the agent's end-to-end internal logic in isolation.
It uses mocking to replace the agent's tools AND the LLM's multi-turn responses,
allowing for predictable and repeatable testing of the agent's reasoning,
tool usage, callback execution, and final state manipulation without making
actual API calls.
"""
import asyncio
import json
from unittest.mock import MagicMock, patch, AsyncMock

import pytest
from google.adk.tools import ToolContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part, FunctionCall
from google.adk.models import LlmResponse

from trade_weaver.sub_agents.market_analyst.agent import market_analyst_agent
from trade_weaver.sub_agents.market_analyst.schemas import MarketRegimeState

# --- Test Constants ---
APP_NAME = "test_market_analyst_app"
USER_ID = "test_user_unit"
SESSION_ID = "test_session_unit"

MOCK_USER_PAYLOAD = json.dumps({
    "target_agent": "market_analyst",
    "parameters": {
        "market_proxy": "SPY",
        "adx_period": 14
    }
})

EXPECTED_REGIME_STATE = MarketRegimeState(
    vix_value=15.0,
    vix_state="Low Volatility",
    adx_value=28.0,
    adx_state="Trending",
    time_state="Regular Trading Hours",
    regime_code="LV-T-RTH",
)

# --- Mock LLM Responses for a Multi-Turn Conversation ---

# 1. First LLM response: The model decides to call the data-gathering tools.
MOCK_LLM_RESPONSE_1_TOOL_CALL = LlmResponse(content=Content(parts=[
    Part(function_call=FunctionCall(name="get_vix_data", args={})),
    Part(function_call=FunctionCall(name="get_adx_data", args={})),
    Part(function_call=FunctionCall(name="get_current_time", args={})),
]))

# 2. Second LLM response: After getting tool results, the model generates its
#    analysis and the JSON block. This is the critical response that the
#    `after_model_callback` will parse.
MOCK_LLM_RESPONSE_2_ANALYSIS = LlmResponse(content=Content(parts=[
    Part(text=f"""
The market regime has been analyzed.
```json
{EXPECTED_REGIME_STATE.model_dump_json()}
```
Proceeding to persist the analysis.
"""),
]))

# 3. Third LLM response: After the callback saves the state, the agent's prompt
#    guides the model to call the final persist tool.
MOCK_LLM_RESPONSE_3_PERSIST_CALL = LlmResponse(content=Content(parts=[
    Part(function_call=FunctionCall(name="persist_market_regime", args={})),
]))


@pytest.mark.asyncio
@patch("google.adk.models.base_llm.BaseLlm.generate_content_async")
async def test_market_analyst_internal_workflow(mock_generate_content: AsyncMock):
    """
    Tests the full internal workflow by mocking the LLM's multi-turn responses
    and all tool executions, verifying the callback-driven state pipeline.
    """
    # --- 1. Mock Setup ---
    mock_vix_tool = MagicMock(return_value={"status": "success", "vix_value": 15.0})
    mock_adx_tool = MagicMock(return_value={"status": "success", "adx_value": 28.0})
    mock_time_tool = MagicMock(return_value={"status": "success", "time_of_day": "10:00:00"})
    mock_persist_tool = MagicMock(return_value={"status": "success", "persisted": True})

    with patch.object(market_analyst_agent, "tools", [mock_vix_tool, mock_adx_tool, mock_time_tool, mock_persist_tool]):
        # Configure the mock LLM to return a sequence of pre-defined responses.
        mock_generate_content.side_effect = [
            MOCK_LLM_RESPONSE_1_TOOL_CALL,
            MOCK_LLM_RESPONSE_2_ANALYSIS,
            MOCK_LLM_RESPONSE_3_PERSIST_CALL,
        ]

        # --- 2. Runner and Session Setup ---
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(
        agent=market_analyst_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # --- 3. Agent Execution ---
    user_message = Content(role="user", parts=[Part(text=MOCK_USER_PAYLOAD)])

    # Consume the entire event stream to drive the agent's execution to completion
    async for _ in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_message):
        pass

    # --- 4. Assertions ---
    # Verify that all tools were called exactly once.
    mock_vix_tool.assert_called_once()
    mock_adx_tool.assert_called_once()
    mock_time_tool.assert_called_once()
    mock_persist_tool.assert_called_once()

    # This is the most important assertion:
    # Check that the `tool_context` passed to the `persist_market_regime` tool
    # contained the correctly parsed and validated data from the `after_model_callback`.
    call_args, call_kwargs = mock_persist_tool.call_args
    assert "tool_context" in call_kwargs
    tool_context_arg: ToolContext = call_kwargs["tool_context"]

    persisted_state_from_context = tool_context_arg.state.get("intermediate_market_regime")

    assert persisted_state_from_context is not None, \
        "Callback failed to save state for the persist tool to use."
    assert persisted_state_from_context == EXPECTED_REGIME_STATE.model_dump()
