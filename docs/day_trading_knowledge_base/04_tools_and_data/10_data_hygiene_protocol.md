# [CONCEPT: Data_Hygiene] Data Hygiene and Preparation Protocol

This document outlines the mandatory, systematic protocol for cleaning and preparing all financial time-series data before it is used by any module of the AI agent. The principle is simple: a trading model is only as reliable as the data it is trained on. Garbage in, garbage out.

### [PRINCIPLE: Importance] The Critical Importance of Data Hygiene

Financial data is notoriously noisy. It is plagued by errors, gaps, and biases that can invalidate backtests and cause live strategies to fail catastrophically. A rigorous data hygiene pipeline is not optional; it is a foundational requirement for any quantitative trading system.

### [PIPELINE: Protocol] The Data Hygiene Pipeline

The following steps must be executed in sequence for any new dataset before it is stored in the primary analytical database (e.g., BigQuery).

#### 1. Timestamp Standardization

-   **[TASK]** Convert all timestamps to a single, universal standard: **UTC**.
-   **[RATIONALE]** Eliminates all ambiguity related to different market hours, local time zones, and daylight saving time changes.

#### 2. Handling of Corporate Actions (Splits and Dividends)

-   **[TASK]** All historical price data must be adjusted for corporate actions.
-   **[RATIONALE]** A stock split can make a price series appear to have crashed overnight. A dividend payment causes a predictable drop in price. Using prices that are not adjusted for these events will introduce false signals into any model.
-   **[SOLUTION]** Always use the **Adjusted Close** price provided by a high-quality data vendor like EODHD. This value is retroactively adjusted for all splits and dividends, providing a clean and comparable historical price series.

#### 3. Handling Missing Data (Gaps)

-   **[TASK]** Identify and correct for missing data points, which can arise from exchange halts, data feed errors, or other issues.
-   **[RATIONALE]** Gaps in time-series data can break calculations for indicators and models.
-   **[SOLUTION]** The standard and safest method for handling missing price data is **Forward Fill (ffill)**, also known as Last Observation Carried Forward (LOCF). This method fills a missing value with the last known value, assuming the price has not changed. This is preferable to interpolation, which can introduce data that never actually existed.

```python
# Example: Forward-filling missing data in a pandas DataFrame
import pandas as pd

# Assume df has a datetime index and a 'close' column with missing values
df['close'] = df['close'].fillna(method='ffill')
```

#### 4. Correcting Erroneous Data (Outliers)

-   **[TASK]** Identify and correct for anomalous data points or "bad ticks."
-   **[RATIONALE]** Data feeds can sometimes contain erroneous prints that are far from the true market price. These outliers can severely skew statistical calculations and model training.
-   **[SOLUTION]** Use a statistical method to detect outliers, such as identifying any data point that is more than a set number of standard deviations (e.g., 5-7 std dev) from a rolling mean. Once identified, these outliers should be treated as missing data and corrected using the forward-fill method.

#### 5. Addressing Survivorship Bias

-   **[TASK]** Ensure the historical dataset includes delisted securities.
-   **[RATIONALE]** Survivorship bias is a subtle but fatal flaw where a dataset only includes companies that "survived." This inflates historical performance metrics because it ignores all the companies that failed.
-   **[SOLUTION]** Use a data provider (like EODHD) that provides a **point-in-time database**, which includes data for all securities that were trading at any given point in the past, including those that were later delisted.

### [CONCEPT: ADK_Implementation] ADK Implementation Pattern

-   **[ARCHITECTURE]** This entire protocol should be implemented as a dedicated, event-driven data validation service (e.g., a GCP Cloud Function or Cloud Run service). This service is triggered whenever new data is ingested (either from a real-time feed or a batch download). It runs through the full hygiene pipeline before writing the clean, validated data to the final analytical database. This ensures that all other modules in the system only ever have access to clean data.

[SOURCE_ID: Data Hygiene for Financial Time Series Data Research]
