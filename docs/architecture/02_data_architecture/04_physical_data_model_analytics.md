# Physical Data Model: Analytics Warehouse

This document defines the physical schemas for the tables in the analytics data warehouse, which will be implemented in **Google BigQuery**. These tables are designed for efficient querying to support backtesting and machine learning model training.

## 1. Raw Market Data Table

This table stores the raw, time-series data as it is ingested from the providers. It is optimized for write-heavy workloads and serves as the immutable source of truth.

-   **Table Name:** `raw_market_data`
-   **Partitioning:** Partitioned by `event_date` (Day).
-   **Clustering:** Clustered by `ticker`.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `ticker` | `STRING` | The instrument ticker symbol. |
| `event_timestamp_utc` | `TIMESTAMP` | The precise timestamp of the event (e.g., the start of a 1-minute bar). |
| `event_date` | `DATE` | The date of the event, used for partitioning. |
| `open` | `FLOAT64` | The opening price for the bar. |
| `high` | `FLOAT64` | The highest price for the bar. |
| `low` | `FLOAT64` | The lowest price for the bar. |
| `close` | `FLOAT64` | The closing price for the bar. |
| `volume` | `INT64` | The volume for the bar. |
| `source` | `STRING` | The data provider source (e.g., 'EODHD', 'IBKR'). |

## 2. Instrument Features Table

This table stores the calculated features and technical indicators for each instrument at each time step. This is the primary table used as the input for training machine learning models.

-   **Table Name:** `instrument_features`
-   **Partitioning:** Partitioned by `feature_date` (Day).
-   **Clustering:** Clustered by `ticker`.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `ticker` | `STRING` | The instrument ticker symbol. |
| `feature_timestamp_utc` | `TIMESTAMP` | The timestamp for which the features are calculated. |
| `feature_date` | `DATE` | The date of the feature calculation, used for partitioning. |
| `rsi_14d` | `FLOAT64` | The 14-day Relative Strength Index. |
| `ema_9d` | `FLOAT64` | The 9-day Exponential Moving Average. |
| `ema_20d` | `FLOAT64` | The 20-day Exponential Moving Average. |
| `bb_upper_20d_2std` | `FLOAT64` | The upper Bollinger Band. |
| `bb_lower_20d_2std` | `FLOAT64` | The lower Bollinger Band. |
| `atr_14d` | `FLOAT64` | The 14-day Average True Range. |
| `log_return_1d` | `FLOAT64` | The 1-day log return, used for volatility calculations. |
| `sentiment_score_1h` | `FLOAT64` | The rolling 1-hour average sentiment score from news. |
