# /market_analyst/agent.py
import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator, List, Dict, Any, cast

from google.adk.agents import BaseAgent, ParallelAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.tools import FunctionTool
from google.adk.tools import ToolContext
from google.genai import types as genai_types

from market_analyst.sub_agents.exchange_gapper_discovery.agent import ExchangeGapperDiscovery
from market_analyst.sub_agents.ticker_enrichment_pipeline.agent import TickerEnrichmentPipeline
from market_analyst.schemas import MarketAnalysisReport, ExchangeReport, MarketRegime, ObservedInstrument
from market_analyst.tools import cluster_instruments

class MarketAnalysisCoordinator(BaseAgent):
    """
    Orchestrates the market analysis pipeline. This agent is STATELESS.
    
    Uses BaseAgent for complex, programmatic control of the multi-stage pipeline
    according to ADK workflow orchestration patterns.
    """

    async def _run_async_impl(
        self,
        ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None]:
        """
        Executes the three-stage market analysis pipeline:
        1. Parallel gapper discovery across exchanges
        2. Parallel ticker enrichment 
        3. Instrument clustering and final report generation
        """

        # Parse input from user message if session state is empty
        if not ctx.session.state.get("exchanges"):
            try:
                import json
                # Get the latest user message
                user_events = [e for e in ctx.session.events if e.content.role == "user"]
                if user_events:
                    latest_user_event = user_events[-1]
                    if latest_user_event.content.parts:
                        user_text = latest_user_event.content.parts[0].text
                        # Try to parse as JSON
                        if user_text.strip().startswith('{'):
                            input_data = json.loads(user_text)
                            if isinstance(input_data, dict):
                                # Update session state with parsed input
                                ctx.session.state.update(input_data)
                                # Input parsed successfully - no event needed for clean output
            except (json.JSONDecodeError, IndexError, AttributeError) as e:
                yield Event(
                    author=self.name,
                    content=genai_types.Content(parts=[
                        genai_types.Part(text=f"Warning: Could not parse user input as JSON: {str(e)}")
                    ])
                )

        run_type = ctx.session.state.get("run_type", "Pre-Market")
        exchange_ids = ctx.session.state.get("exchanges", [])

        if not exchange_ids:
            yield Event(
                author=self.name, 
                content=genai_types.Content(parts=[
                    genai_types.Part(text="Error: No exchanges provided in session state.")
                ])
            )
            return

        try:
            # --- Stage 1: Discover Gappers in Parallel ---
            discovery_agents = [ExchangeGapperDiscovery(exchange_id=eid) for eid in exchange_ids]
            
            # Fix: Cast to List[BaseAgent] to satisfy ParallelAgent type requirements
            discovery_pipeline = ParallelAgent(
                name="gapper_discovery_pipeline", 
                sub_agents=cast(List[BaseAgent], discovery_agents)
            )
            
            async for event in discovery_pipeline.run_async(ctx):
                pass  # Silent - don't yield sub-agent events for clean output

            # --- Fan-In #1: Collect Discovery Results ---
            all_gappers_with_exchange: List[Dict[str, Any]] = []
            exchange_reports_map: Dict[str, ExchangeReport] = {}

            for exchange_id in exchange_ids:
                discovery_result = ctx.session.state.get(f"discovery_{exchange_id}")
                if not discovery_result:
                    # Handle missing discovery results gracefully
                    yield Event(
                        author=self.name,
                        content=genai_types.Content(parts=[
                            genai_types.Part(text=f"Warning: No discovery results for {exchange_id}")
                        ])
                    )
                    continue
                
                # Validate discovery result structure
                if "tickers" not in discovery_result or "market_regime" not in discovery_result:
                    yield Event(
                        author=self.name,
                        content=genai_types.Content(parts=[
                            genai_types.Part(text=f"Error: Invalid discovery result structure for {exchange_id}")
                        ])
                    )
                    continue

                gappers_list = discovery_result["tickers"]
                for gapper in gappers_list:
                    all_gappers_with_exchange.append({**gapper, "exchange_id": exchange_id})
                
                # Create exchange report with market regime data
                try:
                    exchange_reports_map[exchange_id] = ExchangeReport(
                        exchange_id=exchange_id,
                        market_regime=MarketRegime(**discovery_result["market_regime"]),
                        observed_instruments=[],
                    )
                except Exception as e:
                    yield Event(
                        author=self.name,
                        content=genai_types.Content(parts=[
                            genai_types.Part(text=f"Error creating market regime for {exchange_id}: {str(e)}")
                        ])
                    )
                    continue

            # --- Stage 2: Enrich Gappers in Parallel ---
            if not all_gappers_with_exchange:
                # Create an empty report if no gappers were found
                final_report_no_gappers = MarketAnalysisReport(
                    report_id=str(uuid.uuid4()),
                    analysis_timestamp_utc=datetime.now(timezone.utc).isoformat(),
                    run_type=run_type,
                    exchange_reports=list(exchange_reports_map.values()),
                )
                yield Event(
                    author=self.name, 
                    content=genai_types.Content(parts=[
                        genai_types.Part(text=final_report_no_gappers.model_dump_json(indent=2))
                    ])
                )
                return

            enrichment_agents = [
                TickerEnrichmentPipeline(
                    ticker=g['ticker'],
                    exchange_id=g['exchange_id'],
                    gapper_data=g
                ) for g in all_gappers_with_exchange
            ]

            # Fix: Cast to List[BaseAgent] for ParallelAgent
            enrichment_pipeline = ParallelAgent(
                name="enrichment_pipeline", 
                sub_agents=cast(List[BaseAgent], enrichment_agents)
            )
            
            async for event in enrichment_pipeline.run_async(ctx):
                pass  # Silent - don't yield sub-agent events for clean output

            # --- Fan-In #2: Collect Enrichment Results ---
            enriched_instruments_dicts = []
            for gapper in all_gappers_with_exchange:
                enriched_data = ctx.session.state.get(f"enriched_{gapper['ticker']}")
                if enriched_data:
                    enriched_instruments_dicts.append(enriched_data)
                else:
                    yield Event(
                        author=self.name,
                        content=genai_types.Content(parts=[
                            genai_types.Part(text=f"Warning: No enrichment data for {gapper['ticker']}")
                        ])
                    )

            if not enriched_instruments_dicts:
                yield Event(
                    author=self.name,
                    content=genai_types.Content(parts=[
                        genai_types.Part(text="Error: No instruments were successfully enriched.")
                    ])
                )
                return

            # --- Stage 3: Cluster Instruments ---
            cluster_tool = FunctionTool(cluster_instruments)
            
            # Fix: Create proper ToolContext from InvocationContext
            # Note: This assumes InvocationContext can be used as ToolContext
            # If not, we may need to extract specific properties
            tool_context = cast(ToolContext, ctx)
            
            try:
                cluster_result = await cluster_tool.run_async(
                    args={"instruments": enriched_instruments_dicts}, 
                    tool_context=tool_context
                )
                clustered_instruments = cluster_result.get("clustered_instruments", [])
            except Exception as e:
                yield Event(
                    author=self.name,
                    content=genai_types.Content(parts=[
                        genai_types.Part(text=f"Error during clustering: {str(e)}")
                    ])
                )
                return

            # Map clustered instruments back to exchange reports
            for instrument_data in clustered_instruments:
                exchange_id = instrument_data.get("exchange_id")
                if exchange_id and exchange_id in exchange_reports_map:
                    try:
                        observed_instrument = ObservedInstrument(**instrument_data)
                        exchange_reports_map[exchange_id].observed_instruments.append(observed_instrument)
                    except Exception as e:
                        yield Event(
                            author=self.name,
                            content=genai_types.Content(parts=[
                                genai_types.Part(text=f"Error creating ObservedInstrument for {instrument_data.get('ticker', 'unknown')}: {str(e)}")
                            ])
                        )
                        continue

            # --- Create and Yield Final Report ---
            try:
                final_report = MarketAnalysisReport(
                    report_id=str(uuid.uuid4()),
                    analysis_timestamp_utc=datetime.now(timezone.utc).isoformat(),
                    run_type=run_type,
                    exchange_reports=list(exchange_reports_map.values()),
                )

                yield Event(
                    author=self.name,
                    content=genai_types.Content(parts=[
                        genai_types.Part(text=final_report.model_dump_json(indent=2))
                    ])
                )
                
            except Exception as e:
                yield Event(
                    author=self.name,
                    content=genai_types.Content(parts=[
                        genai_types.Part(text=f"Error creating final report: {str(e)}")
                    ])
                )

        except Exception as e:
            # Catch-all error handler for unexpected issues
            yield Event(
                author=self.name,
                content=genai_types.Content(parts=[
                    genai_types.Part(text=f"Unexpected error in market analysis pipeline: {str(e)}")
                ])
            )

# Create the root agent instance
root_agent = MarketAnalysisCoordinator(
    name="market_analyst_coordinator",
    description="Orchestrates the market analysis pipeline with robust error handling.",
)