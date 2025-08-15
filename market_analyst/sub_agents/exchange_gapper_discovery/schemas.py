# /market_analyst/sub_agents/exchange_gapper_discovery/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any

class GapperDiscoveryResult(BaseModel):
    tickers: List[Dict[str, Any]]
    market_regime: Dict[str, Any]
