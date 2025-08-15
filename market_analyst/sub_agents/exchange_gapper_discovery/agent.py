# /market_analyst/sub_agents/exchange_gapper_discovery/agent.py
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from google.adk.events import Event
from google.genai import types as genai_types
from .tools import discover_exchange_gappers, get_market_regime
from pydantic import Field

def _sanitize_name(name: str) -> str:
    """Sanitize an exchange name to create a valid Python identifier for agent names."""
    # Replace dots and other invalid characters with underscores
    return name.replace(".", "_").replace("-", "_").replace(" ", "_")

class ExchangeGapperDiscovery(BaseAgent):
    """A sub-agent that discovers gappers for a given exchange."""
    exchange_id: str = Field(..., description="The ID of the exchange to discover gappers for.")

    def __init__(self, **kwargs):
        sanitized_exchange = _sanitize_name(kwargs.get('exchange_id', ''))
        super().__init__(name=f"discover_{sanitized_exchange}", **kwargs)

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
        # Silent worker agent - no events yielded for clean output
        return
        # This line will never be reached, but keeps the AsyncGenerator signature valid
        yield  # pragma: no cover
