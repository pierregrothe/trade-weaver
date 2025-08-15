# /market_analyst/sub_agents/ticker_enrichment_pipeline/agent.py
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator, Dict, Any
from google.adk.events import Event
from google.genai import types as genai_types
from .tools import enrich_ticker_data
from pydantic import Field

def _sanitize_name(name: str) -> str:
    """Sanitize a ticker name to create a valid Python identifier for agent names."""
    # Replace dots and other invalid characters with underscores
    return name.replace(".", "_").replace("-", "_").replace(" ", "_")

class TickerEnrichmentPipeline(BaseAgent):
    ticker: str = Field(..., description="The ticker to enrich.")
    exchange_id: str = Field(..., description="The ID of the exchange the ticker belongs to.")
    gapper_data: Dict[str, Any] = Field(..., description="The gapper data for the ticker.")

    def __init__(self, **kwargs):
        sanitized_ticker = _sanitize_name(kwargs.get('ticker', ''))
        super().__init__(name=f"enrich_{sanitized_ticker}", **kwargs)

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
        # Silent worker agent - no events yielded for clean output
        return
        # This line will never be reached, but keeps the AsyncGenerator signature valid
        yield  # pragma: no cover
