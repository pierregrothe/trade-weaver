# /market_analyst/schemas.py
from pydantic import BaseModel, Field
from typing import List
from .sub_agents.ticker_enrichment_pipeline.schemas import ObservedInstrument

class MarketRegime(BaseModel):
    vix_ticker: str
    vix_value: float
    adx_value: float

class ExchangeReport(BaseModel):
    exchange_id: str
    market_regime: MarketRegime
    observed_instruments: List[ObservedInstrument]

class MarketAnalysisReport(BaseModel):
    report_id: str
    analysis_timestamp_utc: str
    run_type: str
    exchange_reports: List[ExchangeReport]
