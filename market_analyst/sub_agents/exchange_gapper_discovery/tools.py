# /market_analyst/sub_agents/exchange_gapper_discovery/tools.py
import asyncio
from typing import List, Dict, Any

async def discover_exchange_gappers(exchange_id: str) -> List[Dict[str, Any]]:
    """Discovers gapping instruments for a given exchange. Returns a list of ticker dicts."""
    print(f"Discovering gappers for {exchange_id}...")
    await asyncio.sleep(0.2)
    
    # Return different mock data based on exchange to simulate realistic discovery
    if exchange_id == "NASDAQ":
        return [
            {"ticker": "AAPL", "gap_percent": 5.2, "pre_market_volume": 1250000, "relative_volume": 15.3},
            {"ticker": "TSLA", "gap_percent": -2.8, "pre_market_volume": 980000, "relative_volume": 8.7},
        ]
    elif exchange_id == "TSX":
        return [
            {"ticker": "SHOP.TO", "gap_percent": 3.1, "pre_market_volume": 450000, "relative_volume": 12.5},
            {"ticker": "CNR.TO", "gap_percent": -1.5, "pre_market_volume": 320000, "relative_volume": 6.2},
        ]
    else:
        # Default fallback for other exchanges
        return [
            {"ticker": "DEFAULT", "gap_percent": 0.0, "pre_market_volume": 100000, "relative_volume": 1.0},
        ]

async def get_market_regime(exchange_id: str) -> Dict[str, Any]:
    """Gets the market regime for a given exchange. Returns a dictionary."""
    print(f"Getting market regime for {exchange_id}...")
    await asyncio.sleep(0.1)
    vix_ticker = "^VIXC" if exchange_id == "TSX" else "^VIX"
    return {"vix_ticker": vix_ticker, "vix_value": 18.5, "adx_value": 28.1}
