"""
Defines the Market Analyst Agent as a four-step sequential pipeline.

This agent is responsible for analyzing market conditions by orchestrating a
series of sub-agents to fetch, process, and synthesize market data into a
structured `MarketRegimeState` object.
"""
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent

from trade_weaver.config import MODEL_FLASH
from .prompt import INSTRUCTION
from .schemas import MarketRegimeState
from .tools import market_analyst_toolset

from typing import Dict, Any, Optional
from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool

def skip_summarization_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    """
    An after_tool_callback that sets the skip_summarization flag and ensures
    the tool's dictionary output is preserved.
    This prevents the LlmAgent from making a follow-up model call to summarize
    the tool's output, which is crucial for the pipeline's conversational flow.
    It returns the original tool_response to ensure it's correctly processed.
    """
    tool_context.actions.skip_summarization = True
    return tool_response


# --- Step 1: Exchange Info Fetcher Agent ---
# This agent's sole responsibility is to call the tool that fetches
# foundational details about the target exchange.
exchange_info_fetcher_agent = LlmAgent(
    name="exchange_info_fetcher",
    description="Fetches key details for a given stock exchange.",
    model=MODEL_FLASH,
    instruction="Given the 'exchange' parameter, call the `get_exchange_details` tool and then you are done.",
    tools=[market_analyst_toolset.get_exchange_details_tool],
    after_tool_callback=skip_summarization_callback,
)

# --- Step 2: Data Gatherer Agent (Parallel) ---
# This agent runs multiple data-gathering tools concurrently for maximum efficiency.
# It relies on the 'exchange_details' being present in the session state from Step 1.
data_gatherer_agent = ParallelAgent(
    name="data_gatherer",
    description="Gathers various market data points in parallel.",
    sub_agents=[
        # Each of these is a "headless" LlmAgent designed to call one specific tool.
        LlmAgent(
            name="vix_fetcher",
            description="Fetches VIX data.",
            model=MODEL_FLASH,
            instruction="Call the `get_vix_data` tool and you are done.",
            tools=[market_analyst_toolset.get_vix_data_tool],
            after_tool_callback=skip_summarization_callback,
        ),
        LlmAgent(
            name="adx_fetcher",
            description="Fetches ADX data.",
            model=MODEL_FLASH,
            instruction="Call the `get_adx_data` tool and you are done.",
            tools=[market_analyst_toolset.get_adx_data_tool],
            after_tool_callback=skip_summarization_callback,
        ),
        LlmAgent(
            name="time_fetcher",
            description="Fetches the current time for the exchange.",
            model=MODEL_FLASH,
            instruction="Call the `get_current_time` tool and you are done.",
            tools=[market_analyst_toolset.get_current_time_tool],
            after_tool_callback=skip_summarization_callback,
        ),
    ],
)

# --- Step 3: Synthesizer Agent ---
# This agent takes all the data gathered in the previous steps and synthesizes it
# into the final, structured `MarketRegimeState` object.
synthesizer_agent = LlmAgent(
    name="synthesizer",
    description="Synthesizes gathered data into a final market regime analysis.",
    model=MODEL_FLASH,
    instruction=INSTRUCTION,  # The detailed prompt from prompt.py
    # This agent does not call tools directly; it only synthesizes data.
    # Its output is constrained to the Pydantic schema.
    output_schema=MarketRegimeState,
    output_key="validated_market_regime",
)

# --- Step 4: Persistence Agent ---
# The final step in the pipeline, this agent's only job is to persist the
# validated result produced by the Synthesizer.
persistence_agent = LlmAgent(
    name="persistence",
    description="Persists the final analysis result to a data store.",
    model=MODEL_FLASH,
    instruction="Call the `persist_market_regime` tool to save the result.",
    tools=[market_analyst_toolset.persist_market_regime_tool],
)


# --- The Final Pipeline: Market Analyst Agent (Sequential) ---
# This sequential agent orchestrates the entire workflow, ensuring each step
# is executed in the correct order.
market_analyst_agent = SequentialAgent(
    name="market_analyst_agent",
    description="A pipeline that analyzes and reports on the current market regime.",
    sub_agents=[
        exchange_info_fetcher_agent,
        data_gatherer_agent,
        synthesizer_agent,
        persistence_agent,
    ],
)