# Market Analysis Report: JSON Output Schema

* **Status:** Active
* **Version:** 1.0

## 1. Document Purpose

This document provides the definitive, canonical schema for the `MarketAnalysisReport` JSON object. This object is the **terminal output** of the **Market Analyst Agent** and serves as the primary data input for any downstream consumer, such as a **Strategy & Execution Agent**.

This schema is designed to be a pure, objective data report. It provides raw, quantitative metrics and avoids interpretive states (e.g., "High Volatility"), granting the consuming agent maximum flexibility to apply its own proprietary logic, user-configured thresholds, and strategy-selection models.

## 2. Top-Level JSON Structure

The root of the report is a JSON object containing metadata about the analysis run and an array of exchange-specific reports.

```json
{
  "report_id": "string (UUID)",
  "analysis_timestamp_utc": "string (ISO 8601)",
  "run_type": "string (Enum: Pre-Market, Intraday_Open, Intraday_Midday)",
  "exchange_reports": [
    {
      "exchange_id": "string",
      "market_regime": { "...MarketRegimeObject" },
      "observed_instruments": [
        { "...ObservedInstrumentObject" }
      ]
    }
  ]
}
```

## 3. Detailed Field Breakdown

### 3.1. Market Regime Object (`exchange_reports[].market_regime`)

Contains the raw metrics describing the overall market context for this specific exchange.

| JSON Field (Path) | Data Type | Description & Rationale | Source |
| :--- | :--- | :--- | :--- |
| `vix_ticker` | `string` | The specific VIX ticker used for volatility analysis (e.g., "^VIX", "^VIXC"). Makes the data self-documenting. | Configuration Lookup |
| `vix_value` | `float` | The raw VIX value. Used by the consumer to determine the volatility state. | EODHD Real-Time API |
| `adx_value` | `float` | The raw ADX(14) value of a market proxy. Used by the consumer to determine the trend state. | EODHD Tech Indicators API |

### 3.2. Observed Instrument Object (`exchange_reports[].observed_instruments[]`)

The detailed, objective data for a single financial instrument.

| JSON Field (Path) | Data Type | Description & Rationale | Source |
| :--- | :--- | :--- | :--- |
| `ticker` | `string` | The instrument's ticker symbol. | EODHD Screener API |
| `correlation_cluster_id`| `integer` | An ID assigned by a clustering algorithm (e.g., HRP). Instruments with the same ID are highly correlated. Critical for downstream risk management. | **Internal Calculation** |
| `gapper_data` | `object` | Raw data points quantifying the pre-market gap. | - |
| `gapper_data.gap_percent`| `float` | The percentage gap from the previous day's close. | EODHD Screener API |
| `gapper_data.pre_market_volume` | `integer` | The total volume traded in the pre-market session. | EODHD Screener API |
| `gapper_data.relative_volume` | `float` | Pre-market volume as a multiple of its historical average for that time. The key conviction signal. | EODHD Screener API |
| `risk_metrics` | `object` | Raw data points used for risk filtering and position sizing. | - |
| `risk_metrics.average_true_range_14d` | `float` | The 14-day Average True Range. A key measure of the instrument's volatility. | EODHD Tech Indicators API |
| `risk_metrics.average_dollar_volume_30d` | `float` | The 30-day average daily dollar volume. A key measure of liquidity. | **Internal Calculation** |
| `catalyst_analysis` | `object` | Data related to the news driver behind the instrument's activity. | - |
| `catalyst_analysis.primary_catalyst_type`| `string` | The classification of the most significant recent news (e.g., "Earnings Beat", "M&A Offer"). | **Internal NLP Model** |
| `catalyst_analysis.recent_headlines` | `array` | A list of the raw news headlines used for the analysis. | EODHD News API |
| `key_technical_levels` | `object` | Critical price points derived from pre-market and historical data. | - |
| `key_technical_levels.pre_market_high` | `float` | The highest price reached during the pre-market session. | EODHD Real-Time API |
| `key_technical_levels.pre_market_low` | `float` | The lowest price reached during the pre-market session. | EODHD Real-Time API |
| `key_technical_levels.previous_day_high`| `float` | The high of the previous trading session. | EODHD EOD Historical API |
| `raw_technicals` | `object` | A collection of raw technical indicator values, providing a snapshot of the instrument's state. | - |
| `raw_technicals.vwap` | `float` | The current Volume-Weighted Average Price. | EODHD Tech Indicators API |
| `raw_technicals.rsi_14d` | `float` | The 14-period Relative Strength Index. | EODHD Tech Indicators API |
| `raw_technicals.macd_12_26_9` | `object` | The components of the MACD indicator. | EODHD Tech Indicators API |
| `raw_technicals.ema_9d`, `ema_20d`, `ema_50d` | `float` | Key short, medium, and long-term Exponential Moving Averages. | EODHD Tech Indicators API |
| `raw_technicals.bollinger_bands_20d_2std` | `object` | The components of the Bollinger Bands indicator. | EODHD Tech Indicators API |
| `chart_clarity_raw_components` | `object` | The raw, un-scored component metrics for chart clarity analysis. | - |
| *(all 7 components)* | `float` | See `02a_pre_market_analysis_framework_deep_dive.md` for definitions. | **Internal Calculation** / **Other Provider** (L2/L3) |
| `fundamental_data` | `object` | Basic identifying information for the company. | - |
| `fundamental_data.name`| `string` | The company's full name. | EODHD Fundamentals API |
| `fundamental_data.sector`| `string` | The economic sector the company belongs to. | EODHD Fundamentals API |
| `fundamental_data.industry`| `string` | The specific industry within the sector. | EODHD Fundamentals API |
| `fundamental_data.market_capitalization` | `integer`| The company's market capitalization. | EODHD Fundamentals API |
