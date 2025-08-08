# File: /trade_weaver/sub_agents/market_analyst/agent.py

import inspect
import uuid
from typing import AsyncGenerator, Dict, Any, List

from google.adk.agents import (
    BaseAgent,
    InvocationContext,
    LlmAgent,
    ParallelAgent,
    SequentialAgent,
)
from google.adk.events import Event, EventActions
from google.adk.tools import BaseTool, ToolContext
from google.genai import types as genai_types
from google.genai.types import Content, Part
from pydantic import ConfigDict

from trade_weaver.config import MODEL_FLASH
from trade_weaver.schemas import (
    ExchangeAnalysisResult,
    MarketRegimeState,
    StockCandidateList,
)
from .tools import market_analyst_toolset
from .prompt import INSTRUCTION as REGIME_INSTRUCTION
from .prompt import SCANNER_SYNTHESIS_INSTRUCTION

# --- Reusable Custom Agents for Deterministic Tool Calls ---

class CustomToolCallingAgent(BaseAgent):
    """A custom agent that deterministically calls a single, specific tool."""

    tool: BaseTool
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Logic to call the tool deterministically...
        # (This remains the same as your previous correct version)
        tool_params = inspect.signature(self.tool.func).parameters
        args = {
            param_name: ctx.session.state.get(param_name)
            for param_name in tool_params
            if param_name != "tool_context"
        }
        call_id = f"fn_call_{uuid.uuid4()}"
        function_call = genai_types.FunctionCall(id=call_id, name=self.tool.name, args=args)
        yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(function_call=function_call)]))

        tool_ctx = ToolContext(invocation_context=ctx, function_call_id=call_id, event_actions=EventActions())
        tool_response = await self.tool.run_async(args=args, tool_context=tool_ctx)

        function_response = genai_types.FunctionResponse(id=call_id, name=self.tool.name, response=tool_response)
        yield Event(author=self.name, content=genai_types.Content(role="user", parts=[genai_types.Part(function_response=function_response)]), actions=tool_ctx.actions)


class SetInitialStateAgent(BaseAgent):
    """A deterministic agent that sets the initial state for the pipeline."""
    exchange: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # This agent now directly calls the tool's function to set the state.
        tool = market_analyst_toolset.get_exchange_details_tool
        args = {"exchange": self.exchange}
        tool_ctx = ToolContext(invocation_context=ctx, event_actions=EventActions())
        # We call the tool's function directly to ensure the state is set.
        await tool.run_async(args=args, tool_context=tool_ctx)
        # This agent's job is done, it just yields a confirmation event.
        yield Event(author=self.name, content=Content(parts=[Part(text=f"State initialized for {self.exchange}.")]))



# --- Sub-Pipelines as Classes ---

class MarketRegimeSubPipeline(SequentialAgent):
    """A pipeline to determine the market regime for an exchange."""
    def __init__(self, **kwargs):
        # **CRITICAL:** Sub-agents are INSTANTIATED HERE, inside __init__.
        data_gatherer = CustomToolCallingAgent(
            name="regime_data_gatherer",
            tool=market_analyst_toolset.get_market_regime_data_tool
        )
        regime_synthesizer = LlmAgent(
            name="regime_synthesizer",
            model=MODEL_FLASH,
            instruction=REGIME_INSTRUCTION,
            output_schema=MarketRegimeState,
            output_key="validated_market_regime",
        )
        # We pass the list of INSTANCES to the parent constructor.
        super().__init__(
            name="market_regime_sub_pipeline",
            sub_agents=[data_gatherer, regime_synthesizer],
            **kwargs,
        )

class StockScannerSubPipeline(SequentialAgent):
    """A pipeline to scan for and enrich stock candidates."""
    def __init__(self, **kwargs):
        # **CRITICAL:** Sub-agents are INSTANTIATED HERE, inside __init__.
        stock_data_enricher = CustomToolCallingAgent(
            name="stock_data_enricher",
            tool=market_analyst_toolset.find_pre_market_movers_tool
        )
        synthesis_scanner = LlmAgent(
            name="synthesis_scanner",
            model=MODEL_FLASH,
            instruction=SCANNER_SYNTHESIS_INSTRUCTION,
            output_schema=StockCandidateList,
            output_key="candidate_list_object",
        )
        # We pass the list of INSTANCES to the parent constructor.
        super().__init__(
            name="stock_scanner_sub_pipeline",
            sub_agents=[stock_data_enricher, synthesis_scanner],
            **kwargs,
        )

# --- Main Worker Pipeline Class ---

class MarketAnalystPipeline(SequentialAgent):
    """The complete, parameterized pipeline for analyzing a single exchange."""
    exchange: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, exchange: str, **kwargs):
        # **CRITICAL:** The entire sub-agent tree is created uniquely for this instance.
        # When the Coordinator creates two of these, they will be completely independent.
        sub_agents_for_this_instance = [
            SetInitialStateAgent(name=f"initial_state_setter_{exchange}", exchange=exchange),
            MarketRegimeSubPipeline(),
            StockScannerSubPipeline(),
        ]

        super().__init__(
            name=f"market_analyst_pipeline_{exchange}",
            description=f"A full worker pipeline for the {exchange} market.",
            sub_agents=sub_agents_for_this_instance,
            exchange=exchange,
            **kwargs,
        )

# We now export the CLASS itself, not an instance.
# The CoordinatorAgent will be responsible for creating instances.
market_analyst_agent_class = MarketAnalystPipeline
