# /market_analyst/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class GapperData(BaseModel):
    ticker: str
    gap_percent: float
    pre_market_volume: int
    relative_volume: float

class RiskMetrics(BaseModel):
    average_true_range_14d: float
    average_dollar_volume_30d: float

class CatalystAnalysis(BaseModel):
    primary_catalyst_type: str
    recent_headlines: List[str]

class KeyTechnicalLevels(BaseModel):
    pre_market_high: float
    pre_market_low: float
    previous_day_high: float

class Macd(BaseModel):
    macd_line: float
    signal_line: float
    histogram: float

class BollingerBands(BaseModel):
    upper_band: float
    middle_band: float
    lower_band: float
    band_width: float

class RawTechnicals(BaseModel):
    vwap: float
    rsi_14d: float
    macd_12_26_9: Macd
    ema_9d: float
    ema_20d: float
    ema_50d: float
    bollinger_bands_20d_2std: BollingerBands

class ChartClarityComponents(BaseModel):
    range_integrity: float
    price_action_rhythm: float
    volatility_character: float
    volume_profile_structure: float
    volume_trend_confirmation: float
    order_flow_absorption: float
    cumulative_volume_delta: float

class FundamentalData(BaseModel):
    name: str
    sector: str
    industry: str
    market_capitalization: int

class ObservedInstrument(BaseModel):
    ticker: str
    exchange_id: str
    gapper_data: GapperData
    risk_metrics: RiskMetrics
    catalyst_analysis: CatalystAnalysis
    key_technical_levels: KeyTechnicalLevels
    raw_technicals: RawTechnicals
    chart_clarity_raw_components: ChartClarityComponents
    fundamental_data: FundamentalData
    correlation_cluster_id: Optional[int] = None

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
