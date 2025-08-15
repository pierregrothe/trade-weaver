import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

@pytest.mark.asyncio
async def test_market_analyst_agent():
    """
    Tests the market_analyst agent using the evaluation set.
    This test validates the agent's orchestration and final output structure.
    """
    await AgentEvaluator.evaluate(
        agent_module="market_analyst",
        eval_dataset_file_path_or_dir="tests/evaluation_set.json",
    )
