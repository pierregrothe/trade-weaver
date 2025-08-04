# File: src/trade_weaver/agents/analyzer_agent/agent.py (Definitive Version)

from google.adk.agents import Agent

# Import the decoupled prompt and the shared tool
from .prompts import ANALYZER_AGENT_INSTRUCTION
from trade_weaver.tools.market_data_tools import get_market_data

# The 'root_agent' variable is the conventional name ADK looks for.
root_agent = Agent(
    name="analyzer_agent",
    
    # --- THIS IS THE CORRECTED MODEL NAME ---
    # Based on the latest official documentation for function calling.
    model="gemini-2.0-flash",
    
    description="Scans markets for trading opportunities based on pre-defined strategies.",
    instruction=ANALYZER_AGENT_INSTRUCTION,
    tools=[
        get_market_data
    ]
)