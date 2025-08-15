# /market_analyst/sub_agents/exchange_gapper_discovery/tools.py
import asyncio
from typing import List, Dict, Any

async def discover_exchange_gappers(exchange_id: str) -> List[Dict[str, Any]]:
    """Discovers gapping instruments for a given exchange. Returns a list of ticker dicts."""
    print(f"Discovering gappers for {exchange_id}...")
    await asyncio.sleep(0.2)
    return [
        {"ticker": "AAPL", "gap_percent": 5.2, "pre_market_volume": 1250000, "relative_volume": 15.3},
        {"ticker": "GOOG", "gap_percent": -3.1, "pre_market_volume": 850000, "relative_volume": 12.1},
    ]

async def get_market_regime(exchange_id: str) -> Dict[str, Any]:
    """Gets the market regime for a given exchange. Returns a dictionary."""
    print(f"Getting market regime for {exchange_id}...")
    await asyncio.sleep(0.1)
    vix_ticker = "^VIXC" if exchange_id == "TSX" else "^VIX"
    return {"vix_ticker": vix_ticker, "vix_value": 18.5, "adx_value": 28.1}
