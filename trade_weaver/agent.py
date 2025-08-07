# File: /trade_weaver/agent.py
"""
Defines the root Coordinator Agent for the Trade Weaver platform.

This agent serves as the primary orchestrator, delegating tasks to specialist
sub-agents based on the nature of the incoming request.
"""

from google.adk.agents import LlmAgent

# Import the centralized application configuration
from trade_weaver import config

# Import the specific instruction prompt for this agent
from prompt import INSTRUCTION

# --- Sub-Agent Imports ---
# These imports define the "team" that this coordinator manages.
# Note: These files do not exist yet. We will create them in the next steps.
# from .sub_agents.pre_market_scanner.agent import pre_market_scanner_agent
# from .sub_agents.executor.agent import executor_agent


# Define the root agent instance
root_agent = LlmAgent(
    name="coordinator_agent",

    # Use a powerful model for high-level reasoning and delegation.
    model=config.MODEL_PRO,

    description=(
        "The main coordinator agent. Handles task routing to specialist agents "
        "like the pre-market scanner and trade executor."
    ),

    # The instruction prompt is imported from the separate prompts file for clarity.
    instruction=INSTRUCTION,

    # This agent has no tools of its own. Its sole purpose is to delegate.
    tools=[],

    # Define the hierarchy. ADK will use the descriptions of these sub-agents
    # to enable automatic, LLM-driven delegation.
    sub_agents=[
        # pre_market_scanner_agent, # Will be added once defined
        # executor_agent,           # Will be added once defined
    ],
)