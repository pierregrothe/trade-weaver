# File: /trade_weaver/sub_agents/market_analyst/schemas.py
"""
Defines the Pydantic data schemas for the Market Analyst agent.

This ensures that the data structures used for input, output, and internal
state management are well-defined, validated, and self-documenting.
"""
from pydantic import BaseModel, Field


class MarketRegimeState(BaseModel):
    """
    A structured representation of the market's current regime.

    This object encapsulates the analysis performed by the Market Analyst agent,
    providing a clear, machine-readable snapshot that downstream agents can use
    for strategy selection and decision-making.
    """
    exchange: str = Field(
        ...,
        description="The exchange the analysis was performed for (e.g., 'NASDAQ')."
    )
    vix_value: float = Field(
        ...,
        description="The real-time value of the CBOE Volatility Index (VIX)."
    )
    vix_state: str = Field(
        ...,
        description="The classified state of volatility (e.g., 'Low_Volatility', 'Medium_Volatility', 'High_Volatility')."
    )
    adx_value: float = Field(
        ...,
        description="The real-time value of the Average Directional Index (ADX)."
    )
    adx_state: str = Field(
        ...,
        description="The classified state of the market trend (e.g., 'Ranging_Market', 'Trending_Market')."
    )
    time_of_day_state: str = Field(
        ...,
        description="The classified state of the market session time (e.g., 'Opening_Hour', 'Midday_Lull', 'Closing_Hour')."
    )
    regime_code: str = Field(
        ...,
        description="A composite code summarizing the overall market regime (e.g., 'OPENING_TRENDING_MEDIUM_VOL')."
    )
    timestamp: str = Field(
        ...,
        description="The UTC timestamp of when the analysis was performed."
    )
