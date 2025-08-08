# File: /trade_weaver/schemas.py
"""
Defines the Pydantic data models for structured inputs and outputs.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any

from typing import List, Dict, Any, Optional

class AgentTaskPayload(BaseModel):
    """
    Defines the structured JSON payload for an incoming machine-to-machine task.
    """
    target_agent: str = Field(
        description="The name of the specialist sub-agent to delegate the task to."
    )
    parameters: Dict[str, Any] = Field(
        description="A dictionary of parameters to be passed to the target agent's tools."
    )

class MarketRegime(BaseModel):
    """The overall market environment snapshot."""
    vix_value: float
    vix_state: str
    adx_value: float
    adx_state: str
    time_state: str

class CatalystDetail(BaseModel):
    """Details of a specific market catalyst for a stock."""
    type: str
    headline: str
    source: str
    timestamp: str

class PipelineScore(BaseModel):
    """Represents a single named score from a pipeline stage."""
    name: str
    value: float

class StockCandidateObject(BaseModel):
    """
    Detailed schema for each individual stock candidate that is evolved as it
    moves through thepipeline.
    """
    code: str
    name: str
    exchange: str
    sector: str
    industry: str
    adjusted_close: float
    market_capitalization: int
    pre_market_high: float
    pre_market_low: float
    status: str
    status_reason: str
    correlation_cluster_id: str
    pipeline_scores: List[PipelineScore]
    catalyst_details: List[CatalystDetail]

class MarketRegimeState(BaseModel):
    """A structured representation of the market's current regime."""
    exchange: str
    vix_value: float
    vix_state: str
    adx_value: float
    adx_state: str
    time_of_day_state: str
    regime_code: str
    timestamp: str

class StockCandidateList(BaseModel):
    """A wrapper for a list of stock candidates, used for LLM output."""
    candidates: List[StockCandidateObject]

class ExchangeAnalysisResult(BaseModel):
    """The complete analysis result for a single exchange worker pipeline."""
    market_regime: MarketRegimeState
    candidate_list: List[StockCandidateObject]

class DailyWatchlistDocument(BaseModel):
    """
    The final, aggregated watchlist document for a given day, containing
    the analysis results for each scanned exchange.
    """
    analysis_timestamp_utc: str
    exchanges_scanned: List[str]
    analysis_results: List[ExchangeAnalysisResult]