# File: /trade_weaver/agent.py
"""
Defines the root Coordinator Agent which dynamically orchestrates parallel
market analysis pipelines.
"""
import json
import asyncio
from datetime import datetime
from typing import AsyncGenerator, List, Dict, Any

import pytz
from google.adk.agents import BaseAgent, InvocationContext, ParallelAgent
from google.adk.events import Event
from google.genai.types import Content, Part

from .sub_agents.market_analyst.agent import MarketAnalystPipeline
from .schemas import DailyWatchlistDocument, ExchangeAnalysisResult


class CoordinatorAgent(BaseAgent):
    """
    A custom agent that dynamically creates and runs market analysis pipelines
    in parallel for a list of exchanges, then aggregates the results.
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Implements the fan-out/fan-in orchestration logic."""

        def create_final_event(status: str, result: Any) -> Event:
            payload = {
                "status": status,
                "source_agent": self.name,
                "result": result,
            }
            return Event(
                author=self.name,
                content=Content(parts=[Part(text=json.dumps(payload))]),
            )

        # 1. Parse and validate incoming payload
        if not (ctx.user_content and ctx.user_content.parts and ctx.user_content.parts[0].text):
            yield create_final_event("error", {"error_message": "No JSON payload provided."})
            return

        try:
            payload = json.loads(ctx.user_content.parts[0].text)
            parameters = payload.get("parameters", {})
            exchanges = parameters.get("exchanges")
            if not isinstance(exchanges, list) or not exchanges:
                yield create_final_event("error", {"error_message": "'exchanges' parameter must be a non-empty list."})
                return
        except (json.JSONDecodeError, KeyError):
            yield create_final_event("error", {"error_message": "Invalid JSON payload or missing 'exchanges' parameter."})
            return

        # 2. (Fan-Out) Dynamically build the parallel pipeline
        worker_pipelines = [MarketAnalystPipeline(exchange=ex) for ex in exchanges]
        parallel_runner = ParallelAgent(
            name="parallel_market_scanner",
            description="Runs analysis pipelines for multiple exchanges concurrently.",
            sub_agents=worker_pipelines,
        )

        # 3. Execute the parallel pipelines and stream their events
        async for event in parallel_runner.run_async(ctx):
            yield event

        # 4. (Fan-In) Aggregate results from session state
        analysis_results: List[ExchangeAnalysisResult] = []
        for exchange in exchanges:
            result_key = f"result_{exchange}"
            exchange_result = ctx.session.state.get(result_key)
            if exchange_result and isinstance(exchange_result, ExchangeAnalysisResult):
                analysis_results.append(exchange_result)
            else:
                # In a real application, you would log this failure.
                # For now, we just skip the failed pipeline's result.
                yield Event(author=self.name, content=f"Warning: Could not find or validate result for exchange '{exchange}'.")

        # 5. Assemble the final report using the new schema
        final_report = DailyWatchlistDocument(
            analysis_timestamp_utc=datetime.now(pytz.UTC).isoformat(),
            exchanges_scanned=exchanges,
            analysis_results=analysis_results,
        )

        # 6. Yield the final aggregated result
        yield create_final_event("success", final_report.model_dump())


# --- Agent Instantiation ---
# The root agent no longer needs sub-agents defined at initialization,
# as it creates them dynamically.
root_agent = CoordinatorAgent(
    name="trading_desk_coordinator",
    description="The main dynamic coordinator for parallel M2M task execution.",
)
