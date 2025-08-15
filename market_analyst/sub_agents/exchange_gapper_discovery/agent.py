# /market_analyst/sub_agents/exchange_gapper_discovery/agent.py
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from google.adk.events import Event
from google.genai import types as genai_types
from .tools import discover_exchange_gappers, get_market_regime
from pydantic import Field

class ExchangeGapperDiscovery(BaseAgent):
    """A sub-agent that discovers gappers for a given exchange."""

    # --- THE FIX: Declare the parameter as a class field ---
    exchange_id: str = Field(..., description="The ID of the exchange to discover gappers for.")

    def __init__(self, **kwargs):
        # The 'name' is now set dynamically based on the exchange_id passed in kwargs
        super().__init__(name=f"discover_{kwargs.get('exchange_id')}", **kwargs)
        # Pydantic automatically assigns self.exchange_id from the kwargs

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
        # This worker agent completes its task by updating state. It yields no final Event.
        yield Event(author=self.name, content=genai_types.Content(parts=[genai_types.Part(text="Done")]))
