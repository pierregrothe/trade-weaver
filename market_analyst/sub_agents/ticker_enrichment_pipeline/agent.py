# /market_analyst/sub_agents/ticker_enrichment_pipeline/agent.py
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator, Dict, Any
from google.adk.events import Event
from .tools import enrich_ticker_data

class TickerEnrichmentPipeline(BaseAgent):
    def __init__(self, ticker: str, exchange_id: str, gapper_data: Dict[str, Any], **kwargs):
        super().__init__(name=f"enrich_{ticker}", **kwargs)
        self.ticker = ticker
        self.exchange_id = exchange_id
        self.gapper_data = gapper_data

    async def _run_async_impl(
        self,
        ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None]:

        enriched_data_dict = await enrich_ticker_data(
            ticker=self.ticker,
            exchange_id=self.exchange_id,
            gapper_data=self.gapper_data
        )
        ctx.session.state[f"enriched_{self.ticker}"] = enriched_data_dict
        yield
