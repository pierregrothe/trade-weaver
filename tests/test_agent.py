import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from market_analyst.agent import MarketAnalysisCoordinator
from google.adk.evaluation.eval_set import EvalSet
import uuid
from datetime import datetime, timezone
import json

@pytest.mark.asyncio
async def test_market_analyst_agent():
    """
    Tests the market_analyst agent using the evaluation set.
    """
    await AgentEvaluator.evaluate(
        agent_module="market_analyst",
        eval_dataset_file_path_or_dir="tests/evaluation_set.json",
    )
