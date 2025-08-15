# /market_analyst/sub_agents/exchange_gapper_discovery/tools.py
import asyncio
from typing import List, Dict, Any

from google.adk.events import Event
from google.genai import types

async def discover_exchange_gappers(exchange_id: str) -> Event:
    """
    Discovers gapping instruments for a given exchange.
    This is a mockup function.
    """
    print(f"Discovering gappers for {exchange_id}...")
    await asyncio.sleep(1)  # Simulate network latency
    return Event(
        author="discover_exchange_gappers",
        content=types.Content(
            parts=[
                types.Part(
                    text=str({
                        "tickers": [
                            {"ticker": "AAPL", "gap_percent": 5.2, "pre_market_volume": 1250000, "relative_volume": 15.3},
                            {"ticker": "GOOG", "gap_percent": -3.1, "pre_market_volume": 850000, "relative_volume": 12.1},
                        ]
                    })
                )
            ]
        ),
    )

async def get_market_regime(exchange_id: str) -> Event:
    """
    Gets the market regime for a given exchange.
    This is a mockup function.
    """
    print(f"Getting market regime for {exchange_id}...")
    await asyncio.sleep(0.5)  # Simulate network latency
    return Event(
        author="get_market_regime",
        content=types.Content(
            parts=[
                types.Part(
                    text=str({"vix_ticker": "^VIX", "vix_value": 18.5, "adx_value": 28.1})
                )
            ]
        ),
    )
