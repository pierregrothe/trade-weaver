# /market_analyst/sub_agents/exchange_gapper_discovery/agent.py
from google.adk.agents import SequentialAgent
from google.adk.tools import FunctionTool
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from google.adk.events import Event
from .tools import discover_exchange_gappers, get_market_regime

discover_exchange_gappers_tool = FunctionTool(
    func=discover_exchange_gappers,
)

get_market_regime_tool = FunctionTool(
    func=get_market_regime,
)

from pydantic import Field

class ExchangeGapperDiscovery(SequentialAgent):
    exchange_id: str = Field(..., description="The ID of the exchange to discover gappers for.")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """
    A sub-agent that discovers gappers for a given exchange.
    """

    async def _run_async_impl(
        self,
        ctx: InvocationContext,
    ) -> AsyncGenerator[Event, None]:
        """
        The implementation of the agent's logic.
        """
        gappers_result = await discover_exchange_gappers_tool.run_async(
            args={"exchange_id": self.exchange_id}, tool_context=ctx
        )
        yield gappers_result
        ctx.session.state[f"{self.exchange_id}_gappers"] = gappers_result.content

        market_regime_result = await get_market_regime_tool.run_async(
            args={"exchange_id": self.exchange_id}, tool_context=ctx
        )
        yield market_regime_result
        ctx.session.state[
            f"{self.exchange_id}_market_regime"
        ] = market_regime_result.content

exchange_gapper_discovery_agent = ExchangeGapperDiscovery(name="exchange_gapper_discovery_agent", exchange_id="NASDAQ")
