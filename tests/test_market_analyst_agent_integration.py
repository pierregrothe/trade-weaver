"""
Integration test for the Market Analyst Agent using the ADK AgentEvaluator.
"""
import asyncio
import pytest
from unittest.mock import patch, MagicMock

import google.genai.types as genai_types
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from google.adk.evaluation.eval_case import EvalCase, Invocation, IntermediateData
from google.adk.evaluation.eval_set import EvalSet

from trade_weaver.sub_agents.market_analyst.agent import market_analyst_agent

pytestmark = pytest.mark.asyncio

@patch("trade_weaver.sub_agents.market_analyst.tools.persist_market_regime")
@patch("trade_weaver.sub_agents.market_analyst.tools.get_current_time")
@patch("trade_weaver.sub_agents.market_analyst.tools.get_adx_data")
@patch("trade_weaver.sub_agents.market_analyst.tools.get_vix_data")
async def test_agent_evaluator_trajectory(
    mock_get_vix, mock_get_adx, mock_get_time, mock_persist_regime
):
    """
    Tests the market_analyst_agent's tool-calling sequence using AgentEvaluator.
    """
    mock_get_vix.return_value = {"status": "success", "vix_value": 22.5}
    mock_get_adx.return_value = {"status": "success", "adx_value": 28.1}
    mock_get_time.return_value = {"status": "success", "time_of_day": "10:00:00"}
    mock_persist_regime.return_value = {"status": "success", "persisted": True}

    eval_case = EvalCase(
        eval_id="test_trajectory",
        conversation=[
            Invocation(
                user_content=genai_types.Content(
                    parts=[genai_types.Part(text="Analyze the market regime.")]
                )
            )
        ],
        session_input={
            "app_name": "trade_weaver",
            "user_id": "eval_user",
            "state": {"parameters": {"market_proxy": "SPY", "adx_period": 14}},
        },
    )

    eval_set = EvalSet(
        eval_set_id="market_analyst_trajectory_set",
        eval_cases=[eval_case],
    )

    eval_results_by_eval_id = await AgentEvaluator._get_eval_results_by_eval_id(
        agent_for_eval=market_analyst_agent,
        eval_set=eval_set,
        eval_metrics=[],
        num_runs=1,
    )

    assert "test_trajectory" in eval_results_by_eval_id
    result = eval_results_by_eval_id["test_trajectory"][0]

    assert result.final_eval_status.name != "FAILED", \
        f"Agent inference failed: {result.final_eval_status.name}"
