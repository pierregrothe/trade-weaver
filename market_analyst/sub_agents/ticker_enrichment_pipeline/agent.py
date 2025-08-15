# /market_analyst/sub_agents/ticker_enrichment_pipeline/agent.py
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator, Dict, Any
from google.adk.events import Event
from google.genai import types as genai_types
from .tools import enrich_ticker_data
from pydantic import Field

class TickerEnrichmentPipeline(BaseAgent):
    ticker: str = Field(..., description="The ticker to enrich.")
    exchange_id: str = Field(..., description="The ID of the exchange the ticker belongs to.")
    gapper_data: Dict[str, Any] = Field(..., description="The gapper data for the ticker.")

    def __init__(self, **kwargs):
        super().__init__(name=f"enrich_{kwargs.get('ticker')}", **kwargs)

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
        yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(text="Done")]))
