# /market_analyst/sub_agents/ticker_enrichment_pipeline/agent.py
from google.adk.agents import BaseAgent
from google.adk.tools import FunctionTool
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from google.adk.events import Event
from .tools import enrich_ticker_data

enrich_ticker_data_tool = FunctionTool(
    func=enrich_ticker_data,
)

from pydantic import Field

class TickerEnrichmentPipeline(BaseAgent):
    ticker: str = Field(..., description="The ticker to enrich.")
    gapper_data: dict = Field(..., description="The gapper data for the ticker.")
    exchange_id: str = Field(..., description="The ID of the exchange the ticker belongs to.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def _run_async_impl(
        self,
        ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None]:
        """
        The implementation of the agent's logic.
        """
        enriched_data_result = await enrich_ticker_data_tool.run_async(
            args={
                "ticker": self.ticker,
                "gapper_data": self.gapper_data,
                "exchange_id": self.exchange_id,
            },
            tool_context=ctx,
        )
        yield enriched_data_result
        ctx.session.state[
            f"enriched_{self.ticker}_{self.exchange_id}"
        ] = enriched_data_result.content

ticker_enrichment_pipeline_agent = TickerEnrichmentPipeline(name="ticker_enrichment_pipeline_agent", ticker="AAPL", gapper_data={}, exchange_id="NASDAQ")
