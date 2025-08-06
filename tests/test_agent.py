import pytest
from google.adk.agents import LlmAgent

from trade_weaver.agent import root_agent

@pytest.mark.asyncio
async def test_root_agent_initialization():
    """Tests that the root_agent initializes correctly."""
    assert root_agent is not None, "Root agent should not be None. Check agent initialization and imports."
    assert root_agent.name == "TradingDeskCoordinator"