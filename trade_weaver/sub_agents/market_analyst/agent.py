"""
Defines the Market Analyst Agent as a four-step sequential pipeline.

This agent is responsible for analyzing market conditions by orchestrating a
series of sub-agents to fetch, process, and synthesize market data into a
structured `MarketRegimeState` object.
"""
import inspect
from typing import AsyncGenerator, Dict, Any, Optional

import uuid
from google.genai import types as genai_types
from pydantic import ConfigDict
import uuid
from google.genai import types as genai_types
from pydantic import ConfigDict
from google.adk.agents import BaseAgent, InvocationContext, LlmAgent, ParallelAgent, SequentialAgent
from google.adk.events import Event, EventActions
from google.adk.tools import BaseTool, ToolContext

from trade_weaver.config import MODEL_FLASH
from .prompt import INSTRUCTION
from .schemas import MarketRegimeState
from .tools import market_analyst_toolset


class CustomToolCallingAgent(BaseAgent):
    """A custom agent that deterministically calls a single, specific tool."""

    tool: BaseTool
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """
        Deterministically runs the configured tool by extracting arguments
        from the session state, yielding the appropriate events.
        """
        tool_params = inspect.signature(self.tool.func).parameters
        args = {}
        for param_name in tool_params:
            if param_name != "tool_context":
                if param_name in ctx.session.state:
                    args[param_name] = ctx.session.state[param_name]
                else:
                    yield Event(
                        author=self.name,
                        content=f"Error: Missing required argument '{param_name}' in session state.",
                    )
                    return

        # Manually create and yield the FunctionCall event
        call_id = f"fn_call_{uuid.uuid4()}"
        function_call = genai_types.FunctionCall(id=call_id, name=self.tool.name, args=args)
        yield Event(
            author=self.name,
            invocation_id=ctx.invocation_id,
            content=genai_types.Content(
                role=self.name, parts=[genai_types.Part(function_call=function_call)]
            ),
        )

        # Create a specific ToolContext for the tool call
        tool_ctx = ToolContext(
            invocation_context=ctx,
            function_call_id=call_id,
            event_actions=EventActions(),
        )

        # Await the tool's execution
        tool_response = await self.tool.run_async(args=args, tool_context=tool_ctx)

        # Manually create and yield the FunctionResponse event
        function_response = genai_types.FunctionResponse(
            id=call_id, name=self.tool.name, response=tool_response
        )
        yield Event(
            author=self.name,
            invocation_id=ctx.invocation_id,
            content=genai_types.Content(
                role="user", parts=[genai_types.Part(function_response=function_response)]
            ),
            actions=tool_ctx.actions,
        )


# --- Step 1: Exchange Info Fetcher Agent ---
# This agent's sole responsibility is to call the tool that fetches
# foundational details about the target exchange.
exchange_info_fetcher_agent = CustomToolCallingAgent(
    name="exchange_info_fetcher",
    description="Fetches key details for a given stock exchange.",
    tool=market_analyst_toolset.get_exchange_details_tool,
)

# --- Step 2: Data Gatherer Agent (Parallel) ---
# This agent runs multiple data-gathering tools concurrently for maximum efficiency.
# It relies on the 'exchange_details' being present in the session state from Step 1.
data_gatherer_agent = ParallelAgent(
    name="data_gatherer",
    description="Gathers various market data points in parallel.",
    sub_agents=[
        CustomToolCallingAgent(
            name="vix_fetcher",
            description="Fetches VIX data.",
            tool=market_analyst_toolset.get_vix_data_tool,
        ),
        CustomToolCallingAgent(
            name="adx_fetcher",
            description="Fetches ADX data.",
            tool=market_analyst_toolset.get_adx_data_tool,
        ),
        CustomToolCallingAgent(
            name="time_fetcher",
            description="Fetches the current time for the exchange.",
            tool=market_analyst_toolset.get_current_time_tool,
        ),
    ],
)

# --- Step 3: Synthesizer Agent (NO CHANGE) ---
# This agent remains an LlmAgent because it performs the complex reasoning
# required to synthesize the final analysis from the gathered data.
synthesizer_agent = LlmAgent(
    name="synthesizer",
    description="Synthesizes gathered data into a final market regime analysis.",
    model=MODEL_FLASH,
    instruction=INSTRUCTION,  # The detailed prompt from prompt.py
    output_schema=MarketRegimeState,
    output_key="validated_market_regime",
)

# --- Step 4: Persistence Agent ---
# The final step in the pipeline, this agent's only job is to persist the
# validated result produced by the Synthesizer.
persistence_agent = CustomToolCallingAgent(
    name="persistence",
    description="Persists the final analysis result to a data store.",
    tool=market_analyst_toolset.persist_market_regime_tool,
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