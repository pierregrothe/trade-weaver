# /market_analyst/sub_agents/exchange_gapper_discovery/agent.py
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from google.adk.events import Event
from .tools import discover_exchange_gappers, get_market_regime
from pydantic import Field

class ExchangeGapperDiscovery(BaseAgent):
    exchange_id: str = Field(..., description="The ID of the exchange to discover gappers for.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def _run_async_impl(
        self,
        ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None]:

        gappers_list = await discover_exchange_gappers(self.exchange_id)
        market_regime_dict = await get_market_regime(self.exchange_id)

        ctx.session.state[f"discovery_{self.exchange_id}"] = {
            "tickers": gappers_list,
            "market_regime": market_regime_dict
        }
        yield
