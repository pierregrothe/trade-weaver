"""
Defines the Market Analyst Agent as a highly efficient, deterministic-first
pipeline.

This final refactoring minimizes LLM calls by using custom, code-driven agents
for all deterministic tool-calling tasks. LLMs are now used only for their
essential reasoning and synthesis capabilities, resulting in a faster, more
reliable, and cost-effective system.
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
from .prompt import SCANNER_SYNTHESIS_INSTRUCTION


# --- Deterministic, Reusable Tool-Calling Agents ---

class CustomToolCallingAgent(BaseAgent):
    """
    A deterministic agent that calls a single, specific tool and saves its
    output to a designated key in the session state.
    """
    tool: BaseTool
    output_key: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Deterministically runs the tool and yields the correct events."""
        tool_params = inspect.signature(self.tool.func).parameters
        args = {p: ctx.session.state[p] for p in tool_params if p != "tool_context"}

        call_id = f"fn_call_{uuid.uuid4()}"
        yield Event(
            author=self.name,
            content=genai_types.Content(parts=[genai_types.Part(
                function_call=genai_types.FunctionCall(id=call_id, name=self.tool.name, args=args)
            )])
        )
        tool_ctx = ToolContext(invocation_context=ctx, function_call_id=call_id, event_actions=EventActions())
        tool_response = await self.tool.run_async(args=args, tool_context=tool_ctx)

        # Save the output to the designated state key
        ctx.session.state[self.output_key] = tool_response

        yield Event(
            author=self.name,
            content=genai_types.Content(role="user", parts=[genai_types.Part(
                function_response=genai_types.FunctionResponse(id=call_id, name=self.tool.name, response=tool_response)
            )]),
            actions=tool_ctx.actions
        )

class StockDataEnrichmentAgent(BaseAgent):
    """A deterministic agent that orchestrates the stock enrichment process."""
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Deterministically finds movers and gets details for each one."""
        # 1. Find pre-market movers
        movers_tool = market_analyst_toolset.find_pre_market_movers_tool
        call_id_movers = f"fn_call_{uuid.uuid4()}"
        yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(function_call=genai_types.FunctionCall(id=call_id_movers, name=movers_tool.name, args={}))]))
        tool_ctx_movers = ToolContext(invocation_context=ctx, function_call_id=call_id_movers, event_actions=EventActions())
        movers_response = await movers_tool.run_async(args={}, tool_context=tool_ctx_movers)
        ctx.session.state["pre_market_movers"] = movers_response # Store for synthesis
        yield Event(author=self.name, content=genai_types.Content(role="user", parts=[genai_types.Part(function_response=genai_types.FunctionResponse(id=call_id_movers, name=movers_tool.name, response=movers_response))]), actions=tool_ctx_movers.actions)

        tickers = movers_response.get("tickers", [])
        if not tickers:
            yield Event(author=self.name, content="No pre-market movers found. Ending stock scan.")
            return

        # 2. For each ticker, get full details and aggregate them
        details_tool = market_analyst_toolset.get_full_stock_details_tool
        full_details = {}
        for ticker in tickers:
            call_id_details = f"fn_call_{uuid.uuid4()}"
            args = {"ticker": ticker}
            yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(function_call=genai_types.FunctionCall(id=call_id_details, name=details_tool.name, args=args))]))
            tool_ctx_details = ToolContext(invocation_context=ctx, function_call_id=call_id_details, event_actions=EventActions())
            details_response = await details_tool.run_async(args=args, tool_context=tool_ctx_details)
            if details_response.get("status") == "success":
                full_details[ticker] = details_response.get("details", {})
            yield Event(author=self.name, content=genai_types.Content(role="user", parts=[genai_types.Part(function_response=genai_types.FunctionResponse(id=call_id_details, name=details_tool.name, response=details_response))]), actions=tool_ctx_details.actions)

        # 3. Store the aggregated details in the state
        ctx.session.state["full_stock_details"] = full_details


# --- Sub-Pipelines ---

class MarketRegimeSubPipeline(SequentialAgent):
    """A pipeline to determine the market regime for an exchange."""
    def __init__(self, **kwargs):
        super().__init__(
            name="market_regime_sub_pipeline",
            description="Determines the market regime.",
            sub_agents=[
                ParallelAgent(
                    name="regime_data_gatherer",
                    description="Gathers market regime data in parallel.",
                    sub_agents=[
                        CustomToolCallingAgent(name="vix_fetcher", tool=market_analyst_toolset.get_vix_data_tool, output_key="vix_data"),
                        CustomToolCallingAgent(name="adx_fetcher", tool=market_analyst_toolset.get_adx_data_tool, output_key="adx_data"),
                        CustomToolCallingAgent(name="time_fetcher", tool=market_analyst_toolset.get_current_time_tool, output_key="time_data"),
                    ],
                ),
                LlmAgent(
                    name="regime_synthesizer",
                    description="Synthesizes data into a market regime.",
                    model=MODEL_FLASH,
                    instruction=REGIME_INSTRUCTION,
                    output_schema=MarketRegimeState,
                    output_key="validated_market_regime",
                )
            ],
            **kwargs,
        )

class StockScannerSubPipeline(SequentialAgent):
    """A pipeline to scan for and enrich stock candidates."""
    def __init__(self, **kwargs):
        super().__init__(
            name="stock_scanner_sub_pipeline",
            description="Finds and enriches stock candidates.",
            sub_agents=[
                StockDataEnrichmentAgent(name="stock_data_enricher", description="Deterministically enriches stock data."),
                LlmAgent(
                    name="synthesis_scanner",
                    description="Synthesizes gathered data into a candidate list.",
                    model=MODEL_FLASH,
                    instruction=SCANNER_SYNTHESIS_INSTRUCTION,
                    output_schema=StockCandidateList,
                    output_key="candidate_list_object",
                )
            ],
            **kwargs,
        )

class FinalResultAssemblerAgent(BaseAgent):
    """Assembles the final result from the sub-pipelines."""
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        regime_dict = ctx.session.state.get("validated_market_regime", {})
        candidate_list_dict = ctx.session.state.get("candidate_list_object", {})

        if not regime_dict or not candidate_list_dict:
            yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(text="Error: Missing regime or candidate list in state.")]))
            return

        regime = MarketRegimeState(**regime_dict)
        candidate_list_obj = StockCandidateList(**candidate_list_dict)
        final_result = ExchangeAnalysisResult(market_regime=regime, candidate_list=candidate_list_obj.candidates)

        exchange = regime.exchange
        ctx.session.state[f"result_{exchange}"] = final_result
        yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(text=f"Successfully assembled final result for {exchange}.")]))


# --- Main Worker Pipeline ---

def validate_tool_inputs(
    agent: BaseAgent, ctx: InvocationContext, function_call: genai_types.FunctionCall
) -> None:
    """A callback that validates arguments before a tool is called."""
    if function_call.name == "get_exchange_details":
        exchange = function_call.args.get("exchange")
        if not isinstance(exchange, str) or not exchange.isalnum():
            raise ValueError(
                f"Invalid 'exchange' parameter: '{exchange}'. Must be an alphanumeric string."
            )

class MarketAnalystPipeline(SequentialAgent):
    """The complete, parameterized pipeline for analyzing a single exchange."""
    def __init__(self, exchange: str, **kwargs):
        # The initial state setter is also a deterministic tool call
        set_initial_state = CustomToolCallingAgent(
            name=f"initial_state_setter_{exchange}",
            tool=market_analyst_toolset.get_exchange_details_tool,
            output_key="exchange_details",
        )
        # We need to ensure the 'exchange' parameter is in the state for the tool
        # A small agent to do just that is the cleanest way.
        class SetExchangeParamAgent(BaseAgent):
            async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
                ctx.session.state["exchange"] = exchange
                if False: yield # Required for async generator

        super().__init__(
            name=f"market_analyst_pipeline_{exchange}",
            description=f"A full worker pipeline for the {exchange} market.",
            sub_agents=[
                SetExchangeParamAgent(name=f"set_exchange_param_{exchange}"),
                set_initial_state,
                MarketRegimeSubPipeline(),
                StockScannerSubPipeline(),
                FinalResultAssemblerAgent(name="final_result_assembler"),
            ],
            **kwargs,
        )
        self.before_tool_callback = validate_tool_inputs
