"""
Defines the Market Analyst Agent as a complete, multi-stage pipeline.

This module has been refactored to support a new architecture where this
agent acts as a self-contained worker for a single exchange. It performs a
full analysis, from market regime to stock candidate generation, and assembles
a complete result object.
"""
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
from pydantic import ConfigDict

from trade_weaver.config import MODEL_FLASH
from trade_weaver.schemas import (
    ExchangeAnalysisResult,
    MarketRegimeState,
    StockCandidateList,
)
from .tools import market_analyst_toolset
from .prompt import INSTRUCTION as REGIME_INSTRUCTION

# --- Prompts for Multi-Step Stock Scanning ---
SCANNER_TOOL_INSTRUCTION = """
You are a Research Assistant responsible for data gathering. Your task is to
use the provided tools to collect comprehensive information about promising
stocks for the current exchange.

1.  **First, you MUST use the `find_pre_market_movers` tool** to get an initial
    list of tickers.
2.  **Then, for EACH ticker** from the first step, you MUST use the consolidated
    `get_full_stock_details(ticker)` tool to gather all its information in a
    single, efficient call.

Your job is ONLY to call the tools and gather data. The next agent will perform
the analysis. Make sure you call all required tools for all movers.
"""

SCANNER_SYNTHESIS_INSTRUCTION = """
You are a Senior Analyst. The research assistant has gathered raw data and
stored it in the session state under the keys `pre_market_movers` and
`full_stock_details`.

Your task is to carefully review all of this raw data and synthesize it into a
final, structured list of high-quality `StockCandidateObject`s.

- For each ticker in `pre_market_movers`, find its corresponding data in the
  `full_stock_details` state key.
- Construct a `StockCandidateObject` for each promising ticker, filling in ALL
  required fields based on the data provided.
- The `pipeline_scores` field MUST be a list of objects, where each object has a `name` and a `value`.
- Provide a clear, data-driven `rationale` and `initial_trade_idea` for each
  candidate you select.
- Output the final result as a `StockCandidateList`.
"""


# --- Reusable Custom Agents ---

class CustomToolCallingAgent(BaseAgent):
    """A custom agent that deterministically calls a single, specific tool."""
    tool: BaseTool
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        tool_params = inspect.signature(self.tool.func).parameters
        args = {}
        # This logic is simplified; it assumes no arguments are needed if not in state
        for param_name in tool_params:
            if param_name != "tool_context" and param_name in ctx.session.state:
                args[param_name] = ctx.session.state[param_name]

        call_id = f"fn_call_{uuid.uuid4()}"
        function_call = genai_types.FunctionCall(id=call_id, name=self.tool.name, args=args)
        yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(function_call=function_call)]))

        tool_ctx = ToolContext(invocation_context=ctx, function_call_id=call_id, event_actions=EventActions())
        tool_response = await self.tool.run_async(args=args, tool_context=tool_ctx)

        function_response = genai_types.FunctionResponse(id=call_id, name=self.tool.name, response=tool_response)
        yield Event(author=self.name, content=genai_types.Content(role="user", parts=[genai_types.Part(function_response=function_response)]), actions=tool_ctx.actions)


class SetInitialStateAgent(BaseAgent):
    """A deterministic agent that sets initial state for the pipeline."""
    exchange: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Calls the get_exchange_details tool to populate the state."""
        tool = market_analyst_toolset.get_exchange_details_tool
        args = {"exchange": self.exchange}

        call_id = f"fn_call_{uuid.uuid4()}"
        function_call = genai_types.FunctionCall(id=call_id, name=tool.name, args=args)
        yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(function_call=function_call)]))

        tool_ctx = ToolContext(invocation_context=ctx, function_call_id=call_id, event_actions=EventActions())
        tool_response = await tool.run_async(args=args, tool_context=tool_ctx)

        function_response = genai_types.FunctionResponse(id=call_id, name=tool.name, response=tool_response)
        yield Event(author=self.name, content=genai_types.Content(role="user", parts=[genai_types.Part(function_response=function_response)]), actions=tool_ctx.actions)


# --- Sub-Pipelines ---

class MarketRegimeSubPipeline(SequentialAgent):
    """A pipeline to determine the market regime for an exchange."""
    def __init__(self, **kwargs):
        data_gatherer = ParallelAgent(
            name="regime_data_gatherer",
            description="Gathers market regime data in parallel.",
            sub_agents=[
                CustomToolCallingAgent(name="vix_fetcher", description="Fetches VIX data.", tool=market_analyst_toolset.get_vix_data_tool),
                CustomToolCallingAgent(name="adx_fetcher", description="Fetches ADX data.", tool=market_analyst_toolset.get_adx_data_tool),
                CustomToolCallingAgent(name="time_fetcher", description="Fetches exchange time.", tool=market_analyst_toolset.get_current_time_tool),
            ],
        )
        regime_synthesizer = LlmAgent(
            name="regime_synthesizer",
            description="Synthesizes data into a market regime.",
            model=MODEL_FLASH,
            instruction=REGIME_INSTRUCTION,
            output_schema=MarketRegimeState,
            output_key="validated_market_regime",
        )
        super().__init__(
            name="market_regime_sub_pipeline",
            description="Determines the market regime.",
            sub_agents=[data_gatherer, regime_synthesizer],
            **kwargs,
        )

class StockScannerSubPipeline(SequentialAgent):
    """A pipeline to scan for and enrich stock candidates."""
    def __init__(self, **kwargs):
        tool_calling_scanner = LlmAgent(
            name="tool_calling_scanner",
            description="Calls tools to gather stock data.",
            model=MODEL_FLASH,
            instruction=SCANNER_TOOL_INSTRUCTION,
            tools=[
                market_analyst_toolset.find_pre_market_movers_tool,
                market_analyst_toolset.get_full_stock_details_tool,
            ],
        )
        synthesis_scanner = LlmAgent(
            name="synthesis_scanner",
            description="Synthesizes gathered data into a candidate list.",
            model=MODEL_FLASH,
            instruction=SCANNER_SYNTHESIS_INSTRUCTION,
            output_schema=StockCandidateList,
            output_key="candidate_list_object",
        )
        super().__init__(
            name="stock_scanner_sub_pipeline",
            description="Finds and enriches stock candidates in two steps.",
            sub_agents=[tool_calling_scanner, synthesis_scanner],
            **kwargs,
        )

class FinalResultAssemblerAgent(BaseAgent):
    """Assembles the final result from the sub-pipelines."""
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        regime_dict = ctx.session.state.get("validated_market_regime")
        candidate_list_dict = ctx.session.state.get("candidate_list_object")

        if not regime_dict or not candidate_list_dict:
            yield Event(author=self.name, content="Error: Missing regime or candidate list in state.")
            return

        # Explicitly parse the dicts from state into Pydantic objects
        regime = MarketRegimeState(**regime_dict)
        candidate_list_obj = StockCandidateList(**candidate_list_dict)

        final_result = ExchangeAnalysisResult(
            market_regime=regime,
            candidate_list=candidate_list_obj.candidates,
        )

        # The key here must match what the CoordinatorAgent expects
        exchange = regime.exchange
        ctx.session.state[f"result_{exchange}"] = final_result

        from google.genai.types import Content, Part
        yield Event(
            author=self.name,
            content=Content(
                parts=[
                    Part(text=f"Successfully assembled final result for {exchange}.")
                ]
            )
        )


# --- Main Worker Pipeline ---

class MarketAnalystPipeline(SequentialAgent):
    """The complete, parameterized pipeline for analyzing a single exchange."""
    exchange: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, exchange: str, **kwargs):
        super().__init__(
            name=f"market_analyst_pipeline_{exchange}",
            description=f"A full worker pipeline for the {exchange} market.",
            sub_agents=[
                SetInitialStateAgent(name=f"initial_state_setter_{exchange}", description="Sets initial state.", exchange=exchange),
                MarketRegimeSubPipeline(),
                StockScannerSubPipeline(),
                FinalResultAssemblerAgent(name="final_result_assembler", description="Assembles the final result."),
            ],
            exchange=exchange,
            **kwargs,
        )
