# Value Stream Analysis

This document outlines the primary value streams of the Trade Weaver platform. A value stream is the sequence of activities required to deliver a specific outcome to the end-user or the system itself. Understanding these streams is crucial for identifying opportunities for optimization and automation.

## 1. Pre-Market Analysis & Watchlist Generation

This value stream transforms raw market data into a focused, actionable watchlist of high-probability trading candidates for the upcoming session.

- **Trigger:** Scheduled time (e.g., 7:00 AM ET).
- **Activities:**
    1. **Data Ingestion:** Gather foundational data (EOD prices, fundamentals, news) from EODHD.
    2. **Universe Filtering:** Apply static filters (volume, price, ATR) to define the tradable universe.
    3. **Dynamic Scanning (Fan-Out 1):** In parallel for each exchange, scan the universe for dynamic gappers based on pre-market volume and price changes.
    4. **Candidate Enrichment (Fan-Out 2):** In parallel for each identified gapper, enrich the candidate with deep data (news catalyst analysis, fundamental data, raw technicals).
    5. **Risk Analysis:** Calculate a correlation matrix for all enriched candidates to identify correlated risk clusters.
    6. **Aggregation (Fan-In):** Consolidate the results from all parallel analyses.
- **Outcome:** A single, structured `MarketAnalysisReport` JSON object containing all objective data for the downstream agents.

## 2. Intraday Trading & Execution

This value stream consumes the analysis report, makes trading decisions, and manages the position lifecycle.

- **Trigger:** Market Open event (e.g., 9:30 AM ET).
- **Activities:**
    1. **State Ingestion:** Consume the `MarketAnalysisReport`.
    2. **Strategy Selection:** Apply the dynamic strategy selection matrix based on the current market regime.
    3. **Signal Generation:** The selected strategy module processes the instrument data to generate entry signals.
    4. **Risk Governance:** All signals are passed to the Risk Governor for pre-trade validation and position sizing.
    5. **Order Execution:** Validated orders are sent to the broker via the `BrokerInterface`.
    6. **Position Management:** The agent's Finite State Machine (FSM) manages the open position, tracking against stop-loss and take-profit levels.
- **Outcome:** A series of executed trades, with their results logged to the `Trades` database.

## 3. Post-Market Review & System Adaptation

This value stream provides the critical feedback loop that enables the system to learn and adapt over time.

- **Trigger:** Market Close event (e.g., 4:00 PM ET).
- **Activities:**
    1. **Performance Journaling:** Log all trade details, including advanced metrics like MFE and MAE.
    2. **KPM Calculation:** Calculate Key Performance Metrics (Profit Factor, Sharpe Ratio) for each strategy.
    3. **Automated Analysis:** The `LoopAgent` analyzes the KPMs against predefined thresholds.
    4. **System Adaptation:** Automatically de-allocate capital from or deactivate underperforming strategies.
    5. **Model Retraining:** Trigger retraining pipelines for the ML models if performance decay is detected.
- **Outcome:** An updated system configuration with optimized parameters and a more robust set of active strategies for the next trading session.
