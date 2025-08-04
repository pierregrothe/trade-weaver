# File: src/trade_weaver/agents/analyzer_agent/agent.py

from google.adk.agents import Agent

# Import the decoupled prompt
from .prompts import ANALYZER_AGENT_INSTRUCTION

# Import the shared tool
from trade_weaver.tools.market_data_tools import get_market_data

# The 'root_agent' variable is the conventional name ADK looks for.
root_agent = Agent(
    name="analyzer_agent",
    model="gemini-2.5-flash",
    description="Scans markets for trading opportunities based on pre-defined strategies.",
    instruction=ANALYZER_AGENT_INSTRUCTION,
    tools=[
        get_market_data
    ]
)