# Data Lifecycle Management

This document defines the policies and procedures for managing the data assets of the Trade Weaver platform throughout their entire lifecycle, from creation to archival and deletion. The goal is to ensure data quality, control storage costs, and meet any potential regulatory requirements.

## 1. Data Governance

-   **Data Steward:** The role of Data Steward is assigned to the lead architect. They are ultimately responsible for the quality, integrity, and security of all data within the platform.
-   **Data Consumers:** All automated agents and services that read data are considered data consumers. They are responsible for reporting any data quality issues they encounter.

## 2. Data Hygiene Protocol

All data ingested into the system, whether real-time or batch, MUST pass through the automated Data Hygiene Pipeline before being made available for consumption by analytical or trading agents. This protocol is detailed in the knowledge base and is summarized here:

1.  **Timestamp Standardization:** All timestamps are converted to and stored in UTC.
2.  **Corporate Action Adjustments:** Historical price data is always adjusted for splits and dividends.
3.  **Missing Data Handling:** Missing time-series data points are handled using the Forward Fill (ffill) method.
4.  **Outlier Correction:** Anomalous data points (e.g., bad ticks) are identified via statistical methods and corrected using forward-fill.
5.  **Survivorship Bias Mitigation:** The primary historical data source (EODHD) includes delisted securities to ensure backtests are free from survivorship bias.

## 3. Data Retention Policy

A tiered retention policy is in effect to balance operational needs with storage costs.

| Data Category | Storage System | Retention Period | Rationale |
| :--- | :--- | :--- | :--- |
| **Agent & Portfolio Configuration** | Firestore (Hot) | Indefinite | Critical for system operation. Must always be available. |
| **Operational Trade Logs** | Firestore (Hot) | 12 Months | Required for recent performance analysis and UI display. |
| **Configuration Audit Trail** | Firestore (Hot) | Indefinite | Immutable log required for compliance and security auditing. |
| **Market Analysis Reports (JSON)** | Cloud Storage (Warm) | 12 Months | Used for debugging and short-term model performance analysis. |
| **Raw Ingested Market Data** | BigQuery (Cold) | 36 Months | Required for long-term backtesting and model retraining. |

## 4. Data Archiving Process

-   **Automated Archiving:** Automated jobs (GCP Cloud Functions triggered by Cloud Scheduler) will run monthly to enforce the retention policy.
-   **Trade Log Archival:** After 12 months, trade logs from Firestore will be exported to Parquet format and archived in a Google Cloud Storage "coldline" bucket for long-term, low-cost storage.
-   **Data Deletion:** Data exceeding its defined retention period in any storage tier will be permanently deleted.
