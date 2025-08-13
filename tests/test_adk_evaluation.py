import pytest
import json
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from google.adk.evaluation.eval_set import EvalSet

@pytest.mark.asyncio
async def test_market_analyst_evaluation():
    """
    Runs the ADK evaluation for the market_analyst agent programmatically.
    This approach ensures the evaluation runs within the same Python
    environment as the tests, avoiding 'module not found' errors.
    """
    try:
        with open("trade_weaver/sub_agents/market_analyst/market_analyst_eval_set.json", "r") as f:
            eval_cases = json.load(f)

        eval_set = EvalSet(
            eval_set_id="market_analyst_eval_set",
            eval_cases=eval_cases
        )

        await AgentEvaluator.evaluate_eval_set(
            agent_module="trade_weaver",
            eval_set=eval_set,
            criteria={"response_match_score": 0.8},
        )
    except Exception as e:
        # If the evaluation fails for any reason, pytest will now show a
        # full, detailed Python traceback, which is much better for debugging.
        pytest.fail(f"AgentEvaluator.evaluate failed with an exception: {e}")
