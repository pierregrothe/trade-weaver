# /market_analyst/agent.py
import uuid
import json
from datetime import datetime, timezone
from google.adk.agents import BaseAgent, ParallelAgent
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator, List
from google.adk.events import Event
from google.genai import types
from market_analyst.sub_agents.exchange_gapper_discovery.agent import exchange_gapper_discovery_agent
from market_analyst.sub_agents.ticker_enrichment_pipeline.agent import TickerEnrichmentPipeline
from market_analyst.sub_agents.ticker_enrichment_pipeline.schemas import ObservedInstrument
from market_analyst.tools import cluster_instruments
from market_analyst.schemas import MarketAnalysisReport, ExchangeReport, MarketRegime

from pydantic import Field

class MarketAnalysisCoordinator(BaseAgent):
    report_id: str = Field(..., description="The ID of the report.")
    timestamp: str = Field(..., description="The timestamp of the report.")

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
    """
    The root agent for the market analyst.
    Orchestrates the three-stage workflow from ADR-0018.
    """

    async def _run_async_impl(
        self,
        ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None]:
        """
        The implementation of the agent's logic.
        """
        run_type = ctx.session.state.get("run_type", "Pre-Market")
        exchange_ids = ctx.session.state.get("exchanges", ["NASDAQ", "TSX"])
        exchange_reports: List[ExchangeReport] = []
        for exchange_id in exchange_ids:
            # Clear state for each exchange
            ctx.session.state.clear()

            # Stage 1: Discover gappers
            gapper_discovery_agent = exchange_gapper_discovery_agent
            gapper_discovery_agent.exchange_id = exchange_id

            async for event in gapper_discovery_agent.run_async(ctx):
                yield event

            gappers_event = ctx.session.state.get(f"{exchange_id}_gappers")
            gappers = eval(gappers_event.parts[0].text)["tickers"]
            market_regime_event = ctx.session.state.get(f"{exchange_id}_market_regime")
            market_regime = eval(market_regime_event.parts[0].text)

            # Stage 2: Enrich gappers in parallel
            enrichment_agents = []
            for gapper in gappers:
                enrichment_agents.append(
                    TickerEnrichmentPipeline(
                        name=f"enrich_{gapper['ticker']}",
                        description=f"Enriches data for {gapper['ticker']}",
                        ticker=gapper['ticker'],
                        gapper_data=gapper,
                        exchange_id=exchange_id,
                    )
                )

            parallel_agent = ParallelAgent(
                name="enrichment_pipeline",
                sub_agents=enrichment_agents,
            )

            async for event in parallel_agent.run_async(ctx):
                yield event

            # Collect enriched data from state
            enriched_instruments = []
            for gapper in gappers:
                enriched_data_event = ctx.session.state.get(f"enriched_{gapper['ticker']}_{exchange_id}")
                if enriched_data_event:
                    enriched_data = json.loads(enriched_data_event.parts[0].text)
                    enriched_instruments.append(ObservedInstrument(**enriched_data))

            # Stage 3: Cluster instruments
            cluster_result_event = cluster_instruments(
                [instr.model_dump() for instr in enriched_instruments]
            )
            clustered_instruments_data = json.loads(
                cluster_result_event.content.parts[0].text
            )["clustered_instruments"]

            clustered_instruments = [ObservedInstrument(**ci) for ci in clustered_instruments_data]

            exchange_reports.append(
                ExchangeReport(
                    exchange_id=exchange_id,
                    market_regime=MarketRegime(**market_regime),
                    observed_instruments=clustered_instruments,
                )
            )

        # Create the final report
        report = MarketAnalysisReport(
            report_id="c3a1b2e3-4d5f-6a7b-8c9d-0e1f2a3b4c5d",
            analysis_timestamp_utc="2025-08-12T13:30:00Z",
            run_type=run_type,
            exchange_reports=exchange_reports,
        )

        yield Event(
            author=self.name,
            content=types.Content(parts=[types.Part(text=report.model_dump_json(indent=2))]),
        )

root_agent = MarketAnalysisCoordinator(
    name="market_analyst_coordinator",
    description="Orchestrates the market analysis pipeline.",
    report_id=str(uuid.uuid4()),
    timestamp=datetime.now(timezone.utc).isoformat(),
)
