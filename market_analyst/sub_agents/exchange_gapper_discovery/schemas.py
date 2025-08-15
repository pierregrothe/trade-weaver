from pydantic import BaseModel, Field
from typing import List

class GapperDiscoveryResult(BaseModel):
    """
    Represents the output of the gapper discovery agent.
    """
    exchange_id: str = Field(..., description="The exchange ID.")
    gappers: List[dict] = Field(..., description="A list of gapping instruments.")
    market_regime: dict = Field(..., description="The market regime.")
