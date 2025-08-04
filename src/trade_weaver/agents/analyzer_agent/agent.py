# File: src/trade_weaver/agents/analyzer_agent/agent.py (Corrected)

from google.adk.agents import Agent

from trade_weaver import config
from .prompts import ANALYZER_AGENT_INSTRUCTION
from trade_weaver.tools.market_scanner_tools import create_tradable_universe

root_agent = Agent(
    name="analyzer_agent",
    model=config.FLASH_MODEL, # Using the correct variable from our config
    description="Scans and filters markets to create a daily watchlist of tradable stocks.",
    instruction=ANALYZER_AGENT_INSTRUCTION,
    tools=[
        create_tradable_universe
    ]
)