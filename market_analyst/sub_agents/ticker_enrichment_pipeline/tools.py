# /market_analyst/sub_agents/ticker_enrichment_pipeline/tools.py
import asyncio
from typing import Dict, Any
from market_analyst.schemas import ObservedInstrument, GapperData, RiskMetrics, CatalystAnalysis, KeyTechnicalLevels, RawTechnicals, Macd, BollingerBands, ChartClarityComponents, FundamentalData


def _get_mock_data_for_ticker(ticker: str, exchange_id: str) -> Dict[str, Any]:
    """Generate ticker-specific mock data for enrichment."""
    
    if ticker == "AAPL":
        return {
            "risk_metrics": RiskMetrics(average_true_range_14d=3.45, average_dollar_volume_30d=15200000000.0),
            "catalyst_analysis": CatalystAnalysis(primary_catalyst_type="Earnings Beat", recent_headlines=["Apple reports record Q3 earnings, iPhone sales surge"]),
            "key_technical_levels": KeyTechnicalLevels(pre_market_high=195.50, pre_market_low=192.00, previous_day_high=191.75),
            "raw_technicals": RawTechnicals(
                vwap=194.88, rsi_14d=68.2,
                macd_12_26_9=Macd(macd_line=1.25, signal_line=1.10, histogram=0.15),
                ema_9d=193.50, ema_20d=192.80, ema_50d=190.10,
                bollinger_bands_20d_2std=BollingerBands(upper_band=196.50, middle_band=192.80, lower_band=189.10, band_width=0.038)
            ),
            "chart_clarity": ChartClarityComponents(range_integrity=0.98, price_action_rhythm=0.95, volatility_character=0.97, volume_profile_structure=0.99, volume_trend_confirmation=0.92, order_flow_absorption=0.0, cumulative_volume_delta=0.0),
            "fundamental_data": FundamentalData(name="Apple Inc.", sector="Technology", industry="Consumer Electronics", market_capitalization=3100000000000)
        }
    elif ticker == "TSLA":
        return {
            "risk_metrics": RiskMetrics(average_true_range_14d=12.75, average_dollar_volume_30d=8900000000.0),
            "catalyst_analysis": CatalystAnalysis(primary_catalyst_type="Production Update", recent_headlines=["Tesla Q3 deliveries miss expectations, stock drops"]),
            "key_technical_levels": KeyTechnicalLevels(pre_market_high=248.20, pre_market_low=242.10, previous_day_high=251.80),
            "raw_technicals": RawTechnicals(
                vwap=245.32, rsi_14d=42.8,
                macd_12_26_9=Macd(macd_line=-2.15, signal_line=-1.85, histogram=-0.30),
                ema_9d=244.10, ema_20d=248.95, ema_50d=255.30,
                bollinger_bands_20d_2std=BollingerBands(upper_band=262.40, middle_band=248.95, lower_band=235.50, band_width=0.108)
            ),
            "chart_clarity": ChartClarityComponents(range_integrity=0.85, price_action_rhythm=0.78, volatility_character=0.92, volume_profile_structure=0.88, volume_trend_confirmation=0.75, order_flow_absorption=0.0, cumulative_volume_delta=0.0),
            "fundamental_data": FundamentalData(name="Tesla Inc.", sector="Consumer Cyclical", industry="Auto Manufacturers", market_capitalization=780000000000)
        }
    elif ticker == "SHOP.TO":
        return {
            "risk_metrics": RiskMetrics(average_true_range_14d=5.85, average_dollar_volume_30d=450000000.0),
            "catalyst_analysis": CatalystAnalysis(primary_catalyst_type="Partnership Announcement", recent_headlines=["Shopify announces new AI-powered merchant tools"]),
            "key_technical_levels": KeyTechnicalLevels(pre_market_high=89.45, pre_market_low=86.20, previous_day_high=87.30),
            "raw_technicals": RawTechnicals(
                vwap=87.95, rsi_14d=58.3,
                macd_12_26_9=Macd(macd_line=0.85, signal_line=0.72, histogram=0.13),
                ema_9d=87.10, ema_20d=85.40, ema_50d=82.95,
                bollinger_bands_20d_2std=BollingerBands(upper_band=92.10, middle_band=85.40, lower_band=78.70, band_width=0.157)
            ),
            "chart_clarity": ChartClarityComponents(range_integrity=0.92, price_action_rhythm=0.89, volatility_character=0.94, volume_profile_structure=0.91, volume_trend_confirmation=0.87, order_flow_absorption=0.0, cumulative_volume_delta=0.0),
            "fundamental_data": FundamentalData(name="Shopify Inc.", sector="Technology", industry="Software - Infrastructure", market_capitalization=112000000000)
        }
    elif ticker == "CNR.TO":
        return {
            "risk_metrics": RiskMetrics(average_true_range_14d=2.95, average_dollar_volume_30d=680000000.0),
            "catalyst_analysis": CatalystAnalysis(primary_catalyst_type="Quarterly Results", recent_headlines=["Canadian National Railway reports steady Q3 volumes"]),
            "key_technical_levels": KeyTechnicalLevels(pre_market_high=142.85, pre_market_low=140.50, previous_day_high=143.20),
            "raw_technicals": RawTechnicals(
                vwap=141.65, rsi_14d=48.7,
                macd_12_26_9=Macd(macd_line=-0.45, signal_line=-0.38, histogram=-0.07),
                ema_9d=141.20, ema_20d=142.10, ema_50d=144.80,
                bollinger_bands_20d_2std=BollingerBands(upper_band=147.30, middle_band=142.10, lower_band=136.90, band_width=0.073)
            ),
            "chart_clarity": ChartClarityComponents(range_integrity=0.96, price_action_rhythm=0.93, volatility_character=0.88, volume_profile_structure=0.95, volume_trend_confirmation=0.91, order_flow_absorption=0.0, cumulative_volume_delta=0.0),
            "fundamental_data": FundamentalData(name="Canadian National Railway Company", sector="Industrials", industry="Railroads", market_capitalization=95000000000)
        }
    else:
        # Default fallback data
        return {
            "risk_metrics": RiskMetrics(average_true_range_14d=1.50, average_dollar_volume_30d=100000000.0),
            "catalyst_analysis": CatalystAnalysis(primary_catalyst_type="General Market Movement", recent_headlines=["Market volatility continues"]),
            "key_technical_levels": KeyTechnicalLevels(pre_market_high=50.00, pre_market_low=48.50, previous_day_high=49.75),
            "raw_technicals": RawTechnicals(
                vwap=49.25, rsi_14d=50.0,
                macd_12_26_9=Macd(macd_line=0.0, signal_line=0.0, histogram=0.0),
                ema_9d=49.00, ema_20d=49.50, ema_50d=50.00,
                bollinger_bands_20d_2std=BollingerBands(upper_band=52.00, middle_band=49.50, lower_band=47.00, band_width=0.101)
            ),
            "chart_clarity": ChartClarityComponents(range_integrity=0.80, price_action_rhythm=0.75, volatility_character=0.70, volume_profile_structure=0.85, volume_trend_confirmation=0.80, order_flow_absorption=0.0, cumulative_volume_delta=0.0),
            "fundamental_data": FundamentalData(name="Unknown Company", sector="Unknown", industry="Unknown", market_capitalization=1000000000)
        }

async def enrich_ticker_data(ticker: str, gapper_data: Dict[str, Any], exchange_id: str) -> Dict[str, Any]:
    """Enriches a ticker with additional data. Returns an ObservedInstrument as a dict."""
    print(f"Enriching ticker data for {ticker}...")
    await asyncio.sleep(0.5)

    # Generate ticker-specific mock data
    ticker_data = _get_mock_data_for_ticker(ticker, exchange_id)
    
    enriched_data = ObservedInstrument(
        ticker=ticker,
        exchange_id=exchange_id,
        gapper_data=GapperData(**gapper_data),
        risk_metrics=ticker_data["risk_metrics"],
        catalyst_analysis=ticker_data["catalyst_analysis"],
        key_technical_levels=ticker_data["key_technical_levels"],
        raw_technicals=ticker_data["raw_technicals"],
        chart_clarity_raw_components=ticker_data["chart_clarity"],
        fundamental_data=ticker_data["fundamental_data"]
    )
    return enriched_data.model_dump()
