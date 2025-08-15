# [CONCEPT: Market_Analysis_Output] Market Analysis Report: JSON Output Schema

* **Status:** Accepted
* **Date:** 2025-08-15
* **Author:** AI Assistant, based on direction from Pierre Grothé

## 1. Document Purpose and Design Philosophy

This document provides the definitive, canonical schema for the `MarketAnalysisReport` JSON object. This object is the terminal output of the **Market Analyst Agent** and serves as the primary data input for any downstream consumer, such as a **Strategy & Execution Agent**.

This schema is designed to be a pure, objective data report. It provides raw, quantitative metrics and avoids interpretive states (e.g., "High Volatility"). This grants the consuming agent maximum flexibility to apply its own proprietary logic, user-configured thresholds, and strategy-selection models. It also includes metadata to ensure data provenance and aid in debugging and versioning.

## 2. Top-Level JSON Structure

The root of the report is a JSON object containing metadata about the analysis run and an array of exchange-specific reports.

```json
{
  "report_id": "string (UUID)",
  "analysis_timestamp_utc": "string (ISO 8601)",
  "schema_version": "string (SemVer e.g., 1.1.0)",
  "run_type": "string (Enum: Pre-Market, Intraday_Open, Intraday_Midday)",
  "exchange_reports": [
    { ... }
  ]
}
```

## 3. Detailed Field Breakdown

### 3.1. Root Object

| JSON Field (Path) | Data Type | Description & Rationale | Source |
| :--- | :--- | :--- | :--- |
| **`report_id`** | `string` | A unique identifier (UUID) for the entire analysis run. Critical for logging, tracing, and idempotency. | Agent Runtime Generation |
| **`analysis_timestamp_utc`**| `string` | The ISO 8601 timestamp for when the analysis was completed. | Agent Runtime Generation |
| **`schema_version`** | `string` | The semantic version of this schema. Crucial for preventing parsing errors in downstream consumers if the schema evolves. | Static Configuration |
| **`run_type`** | `string` | An enum indicating the context of the analysis run (`Pre-Market`, `Intraday_Open`, `Intraday_Midday`). | Initial Request Payload |
| **`exchange_reports`** | `array` | The main data container. Each object in this array is a complete report for a single exchange. | - |

### 3.2. Exchange Report Object (`exchange_reports[]`)

| JSON Field (Path) | Data Type | Description & Rationale | Source |
| :--- | :--- | :--- | :--- |
| `exchange_id` | `string` | The official ID of the exchange being reported on (e.g., "NASDAQ", "TSX"). | Initial Request Payload |
| `market_regime` | `object` | Contains the raw metrics describing the overall market context **for this specific exchange**. | - |
| `market_regime.vix_ticker` | `string` | The specific VIX ticker used for volatility analysis (e.g., "^VIX", "^VIXC"). | Configuration Lookup |
| `market_regime.vix_value` | `float` | The raw VIX value. | EODHD Real-Time API |
| `market_regime.adx_value` | `float` | The raw ADX(14) value of a market proxy. | EODHD Tech Indicators API |
| `observed_instruments` | `array` | An array of all instruments on this exchange that were identified and enriched. | - |

### 3.3. Observed Instrument Object (`observed_instruments[]`)

This object contains all the enriched data for a single financial instrument.

| JSON Field (Path) | Data Type | Description & Rationale | Source |
| :--- | :--- | :--- | :--- |
| `ticker` | `string` | The instrument's ticker symbol. | EODHD Screener API |
| `gapper_data` | `object` | Raw data points quantifying the pre-market gap. | - |
| `gapper_data.gap_percent`| `float` | The percentage gap from the previous day's close. | EODHD Screener API |
| `gapper_data.pre_market_volume` | `integer` | The total volume traded in the pre-market session. | EODHD Screener API |
| `gapper_data.relative_volume` | `float` | Pre-market volume as a multiple of its historical average for that time. The key conviction signal. | EODHD Screener API |
| `risk_metrics` | `object` | Raw data points used for risk filtering and position sizing. | - |
| `risk_metrics.average_true_range_14d` | `float` | The 14-day Average True Range. A key measure of the instrument's volatility. | EODHD Tech Indicators API |
| `risk_metrics.short_interest_percent_float` | `float` | The most recent short interest as a percentage of the float. A key input for the Squeeze Risk Score. | EODHD Fundamentals API |
| `catalyst_analysis` | `object` | Data related to the news driver behind the instrument's activity. | - |
| `catalyst_analysis.primary_catalyst_type`| `string` | The classification of the most significant recent news (e.g., "Earnings Beat", "M&A Offer"). | **Internal NLP Model** |
| `catalyst_analysis.catalyst_score` | `float` | A 1-10 score representing the narrative strength of the catalyst. | **Internal NLP Model** |
| `key_technical_levels` | `object` | Critical price points derived from pre-market and historical data. | - |
| `key_technical_levels.pre_market_high` | `float` | The highest price reached during the pre-market session. | EODHD Real-Time API |
| `key_technical_levels.pre_market_low` | `float` | The lowest price reached during the pre-market session. | EODHD Real-Time API |
| `raw_technicals` | `object` | A collection of raw technical indicator values, providing a snapshot of the instrument's state. | - |
| `raw_technicals.vwap` | `float` | The current Volume-Weighted Average Price. | EODHD Tech Indicators API |
| `raw_technicals.rsi_14d` | `float` | The 14-period Relative Strength Index. | EODHD Tech Indicators API |
| `fundamental_data` | `object` | Basic identifying information for the company. | - |
| `fundamental_data.sector`| `string` | The economic sector the company belongs to. | EODHD Fundamentals API |
| `fundamental_data.market_capitalization` | `integer`| The company's market capitalization. | EODHD Fundamentals API |