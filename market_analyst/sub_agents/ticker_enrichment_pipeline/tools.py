# /market_analyst/sub_agents/ticker_enrichment_pipeline/tools.py
import asyncio
from typing import Dict, Any
from .schemas import ObservedInstrument, GapperData, RiskMetrics, CatalystAnalysis, KeyTechnicalLevels, RawTechnicals, Macd, BollingerBands, ChartClarityComponents, FundamentalData

async def enrich_ticker_data(ticker: str, gapper_data: Dict[str, Any], exchange_id: str) -> Dict[str, Any]:
    """Enriches a ticker with additional data. Returns an ObservedInstrument as a dict."""
    print(f"Enriching ticker data for {ticker}...")
    await asyncio.sleep(0.5)

    enriched_data = ObservedInstrument(
        ticker=ticker,
        exchange_id=exchange_id,
        gapper_data=GapperData(**gapper_data),
        risk_metrics=RiskMetrics(average_true_range_14d=3.45, average_dollar_volume_30d=15200000000.0),
        catalyst_analysis=CatalystAnalysis(primary_catalyst_type="Earnings Beat", recent_headlines=["Apple reports record Q3 earnings..."]),
        key_technical_levels=KeyTechnicalLevels(pre_market_high=195.50, pre_market_low=192.00, previous_day_high=191.75),
        raw_technicals=RawTechnicals(
            vwap=194.88, rsi_14d=68.2,
            macd_12_26_9=Macd(macd_line=1.25, signal_line=1.10, histogram=0.15),
            ema_9d=193.50, ema_20d=192.80, ema_50d=190.10,
            bollinger_bands_20d_2std=BollingerBands(upper_band=196.50, middle_band=192.80, lower_band=189.10, band_width=0.038)
        ),
        chart_clarity_raw_components=ChartClarityComponents(range_integrity=0.98, price_action_rhythm=0.95, volatility_character=0.97, volume_profile_structure=0.99, volume_trend_confirmation=0.92, order_flow_absorption=0.0, cumulative_volume_delta=0.0),
        fundamental_data=FundamentalData(
            name="Apple Inc." if ticker == "AAPL" else "Alphabet Inc.",
            sector="Technology",
            industry="Consumer Electronics" if ticker == "AAPL" else "Internet Content & Information",
            market_capitalization=3100000000000 if ticker == "AAPL" else 2200000000000,
        )
    )
    return enriched_data.model_dump()
