from google.adk.agents import LlmAgent, SequentialAgent

from .sub_agents import (
    post_market_journaling_agent,
    pre_market_scanner_agent,
    trading_session_agent,
)

# The root_agent is the main entry point for the agent application.
# Using a SequentialAgent here is a great pattern for orchestrating a
# clear, step-by-step workflow that mirrors a trading day.
root_agent = SequentialAgent(
    name="trade_weaver_orchestrator",
    description="A master agent that orchestrates the full trading day workflow, from pre-market analysis to post-market journaling.",
    # The `sub_agents` list defines the sequence of execution.
    sub_agents=[
        pre_market_scanner_agent,
        trading_session_agent,
        post_market_journaling_agent,
    ],
)