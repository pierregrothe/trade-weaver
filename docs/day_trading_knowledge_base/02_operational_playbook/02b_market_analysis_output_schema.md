# [CONCEPT: Market_Analysis_Output] Market Analysis Report: JSON Output Schema

* **Status:** Accepted
* **Date:** 2025-08-14
* **Author:** AI Assistant, based on direction from Pierre Grothé

## 1. Document Purpose

This document provides the definitive, canonical schema for the `MarketAnalysisReport` JSON object. This object is the terminal output of the **Market Analyst Agent** and serves as the primary data input for any downstream consumer, such as a **Strategy & Execution Agent**.

This schema is designed to be a pure, objective data report. It provides raw, quantitative metrics and avoids interpretive states, granting the consuming agent maximum flexibility to apply its own proprietary logic, user-configured thresholds, and strategy-selection models.

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
      "market_regime": { ... },
      "observed_instruments": [
        { ... }
      ]
    }
  ]
}
```

## 3. Detailed Field Breakdown

### 3.1. Root Object

| JSON Field (Path) | Data Type | Description & Rationale | Source |
| :--- | :--- | :--- | :--- |
| **`report_id`** | `string` | A unique identifier (UUID) for the entire analysis run. Critical for logging, tracing, and idempotency. | Agent Runtime Generation |
| **`analysis_timestamp_utc`**| `string` | The ISO 8601 timestamp for when the analysis was completed and the report was generated. | Agent Runtime Generation |
| **`run_type`** | `string` | An enum indicating the context of the analysis run (`Pre-Market`, `Intraday_Open`, `Intraday_Midday`). Allows the consumer to know which time-of-day logic to apply. | Initial Request Payload |
| **`exchange_reports`** | `array` | The main data container. Each object in this array is a complete report for a single exchange. | - |

### 3.2. Exchange Report Object (`exchange_reports[]`)

| JSON Field (Path) | Data Type | Description & Rationale | Source |
| :--- | :--- | :--- | :--- |
| `exchange_id` | `string` | The official ID of the exchange being reported on (e.g., "NASDAQ", "TSX"). | Initial Request Payload |
| `market_regime` | `object` | Contains the raw metrics describing the overall market context **for this specific exchange**. | - |
| `market_regime.vix_ticker` | `string` | The specific VIX ticker used for volatility analysis (e.g., "^VIX", "^VIXC"). Makes the data self-documenting. | Configuration Lookup |
| `market_regime.vix_value` | `float` | The raw VIX value. Used by the consumer to determine the volatility state. | EODHD Real-Time API |
| `market_regime.adx_value` | `float` | The raw ADX(14) value of a market proxy. Used by the consumer to determine the trend state. | EODHD Tech Indicators API |
| `observed_instruments` | `array` | An array of all instruments on this exchange that were identified and enriched. | - |

### 3.3. Observed Instrument Object (`observed_instruments[]`)

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

## 4. Example Payload

```json
{
  "report_id": "c3a1b2e3-4d5f-6a7b-8c9d-0e1f2a3b4c5d",
  "analysis_timestamp_utc": "2025-08-12T13:30:00Z",
  "run_type": "Pre-Market",
  "exchange_reports": [
    {
      "exchange_id": "NASDAQ",
      "market_regime": {
        "vix_ticker": "^VIX",
        "vix_value": 18.5,
        "adx_value": 28.1
      },
      "observed_instruments": [
        {
          "ticker": "AAPL",
          "correlation_cluster_id": 1,
          "gapper_data": {
            "gap_percent": 5.2,
            "pre_market_volume": 1250000,
            "relative_volume": 15.3
          },
          "risk_metrics": {
            "average_true_range_14d": 3.45,
            "average_dollar_volume_30d": 15200000000.0
          },
          "catalyst_analysis": {
            "primary_catalyst_type": "Earnings Beat",
            "recent_headlines": ["Apple reports record Q3 earnings..."]
          },
          "key_technical_levels": {
            "pre_market_high": 195.50,
            "pre_market_low": 192.00,
            "previous_day_high": 191.75
          },
          "raw_technicals": {
            "vwap": 194.88,
            "rsi_14d": 68.2,
            "macd_12_26_9": {
              "macd_line": 1.25,
              "signal_line": 1.10,
              "histogram": 0.15
            },
            "ema_9d": 193.50,
            "ema_20d": 192.80,
            "ema_50d": 190.10,
            "bollinger_bands_20d_2std": {
              "upper_band": 196.50,
              "middle_band": 192.80,
              "lower_band": 189.10,
              "band_width": 0.038
            }
          },
          "chart_clarity_raw_components": {
            "range_integrity": 0.98,
            "price_action_rhythm": 0.95,
            "volatility_character": 0.97,
            "volume_profile_structure": 0.99,
            "volume_trend_confirmation": 0.92,
            "order_flow_absorption": 0.0,
            "cumulative_volume_delta": 0.0
          },
          "fundamental_data": {
            "name": "Apple Inc.",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "market_capitalization": 3100000000000
          }
        }
      ]
    }
  ]
}
```
