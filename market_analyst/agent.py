import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator, List, Dict, Any

from google.adk.agents import BaseAgent, ParallelAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.tools import FunctionTool
from google.genai import types as genai_types

from market_analyst.sub_agents.exchange_gapper_discovery.agent import ExchangeGapperDiscovery
from market_analyst.sub_agents.ticker_enrichment_pipeline.agent import TickerEnrichmentPipeline
from market_analyst.schemas import MarketAnalysisReport, ExchangeReport, MarketRegime, ObservedInstrument
from market_analyst.tools import cluster_instruments

class MarketAnalysisCoordinator(BaseAgent):
    """Orchestrates the market analysis pipeline. This agent is STATELESS."""

    async def _run_async_impl(
        self,
        ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None]:

        run_type = ctx.session.state.get("run_type", "Pre-Market")
        exchange_ids = ctx.session.state.get("exchanges", [])

        if not exchange_ids:
            yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(text="Error: No exchanges provided.")]))
            return

        # --- Stage 1: Discover Gappers in Parallel ---
        discovery_agents = [ExchangeGapperDiscovery(exchange_id=eid) for eid in exchange_ids]
        discovery_pipeline = ParallelAgent(name="gapper_discovery_pipeline", sub_agents=discovery_agents)
        async for event in discovery_pipeline.run_async(ctx):
            yield event

        # --- Fan-In #1 ---
        all_gappers_with_exchange: List[Dict[str, Any]] = []
        exchange_reports_map: Dict[str, ExchangeReport] = {}

        for exchange_id in exchange_ids:
            discovery_result = ctx.session.state.get(f"discovery_{exchange_id}")
            if discovery_result:
                gappers_list = discovery_result.get("tickers", [])
                for gapper in gappers_list:
                    all_gappers_with_exchange.append({**gapper, "exchange_id": exchange_id})
                exchange_reports_map[exchange_id] = ExchangeReport(
                    exchange_id=exchange_id,
                    market_regime=MarketRegime(**discovery_result["market_regime"]),
                    observed_instruments=[],
                )

        # --- Stage 2: Enrich Gappers in Parallel ---
        enrichment_agents = [
            TickerEnrichmentPipeline(
                ticker=g['ticker'],
                exchange_id=g['exchange_id'],
                gapper_data=g
            ) for g in all_gappers_with_exchange
        ]

        if not enrichment_agents:
            # Create an empty report if no gappers were found
            final_report_no_gappers = MarketAnalysisReport(
                report_id=str(uuid.uuid4()),
                analysis_timestamp_utc=datetime.now(timezone.utc).isoformat(),
                run_type=run_type,
                exchange_reports=list(exchange_reports_map.values()),
            )
            yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(text=final_report_no_gappers.model_dump_json(indent=2))]))
            return

        enrichment_pipeline = ParallelAgent(name="enrichment_pipeline", sub_agents=enrichment_agents)
        async for event in enrichment_pipeline.run_async(ctx):
            yield event

        # --- Fan-In #2 ---
        enriched_instruments_dicts = []
        for gapper in all_gappers_with_exchange:
            enriched_data = ctx.session.state.get(f"enriched_{gapper['ticker']}")
            if enriched_data:
                enriched_instruments_dicts.append(enriched_data)

        # --- Stage 3: Cluster Instruments ---
        cluster_tool = FunctionTool(cluster_instruments)
        cluster_result = await cluster_tool.run_async(args={"instruments": enriched_instruments_dicts}, tool_context=ctx)
        clustered_instruments = cluster_result.get("clustered_instruments", [])

        for instrument_data in clustered_instruments:
            exchange_id = instrument_data["exchange_id"]
            if exchange_id in exchange_reports_map:
                exchange_reports_map[exchange_id].observed_instruments.append(ObservedInstrument(**instrument_data))

        # --- Create and Yield Final Report ---
        final_report = MarketAnalysisReport(
            report_id=str(uuid.uuid4()),
            analysis_timestamp_utc=datetime.now(timezone.utc).isoformat(),
            run_type=run_type,
            exchange_reports=list(exchange_reports_map.values()),
        )

        yield Event(
            author=self.name,
            content=genai_types.Content(parts=[genai_types.Part(text=final_report.model_dump_json(indent=2))])
        )

root_agent = MarketAnalysisCoordinator(
    name="market_analyst_coordinator",
    description="Orchestrates the market analysis pipeline.",
)
