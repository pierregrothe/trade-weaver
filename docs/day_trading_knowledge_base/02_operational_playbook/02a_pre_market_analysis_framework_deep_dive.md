# [CONCEPT: Pre_Market_Framework] Pre-Market Analysis Framework: A Deep Dive

This document provides the definitive, end-to-end conceptual blueprint for the pre-market analysis and watchlist generation pipeline. It synthesizes and expands upon the principles from the knowledge base, incorporating advanced quantitative metrics and market-specific models.

## 1. Core Algorithmic Workflow: A Dual-Model Approach

The pre-market analysis pipeline must account for the fundamental differences in how various global exchanges operate before the official open. This requires two distinct analytical models:

- **Introspective (Confirmatory) Model:** Used for markets with active pre-market trading (e.g., NASDAQ, NYSE). This model analyzes a stock's *own* pre-market price, volume, and order flow data to *confirm* the quality and conviction of an observed move.

- **Extrospective (Predictive) Model:** Used for markets that use a pre-open auction (e.g., TSX, LSE). Since there is no active trading to analyze, this model ingests data from highly correlated *external* instruments (like US-listed ETFs or commodity futures) to *predict* the likely direction and strength of the opening auction.

## 2. Data Sourcing & Catalyst Identification Playbook

A potent catalyst is the primary driver of pre-market activity. The analysis must move beyond simple news headlines to create a "narrative strength" score by synthesizing signals from a diverse portfolio of traditional and alternative data sources.

### 2.1 Foundational Data (EODHD)

- **Real-Time & Historical Pricing:** The primary source for L1 real-time data via WebSockets and deep historical data for calculating baseline metrics.
- **Fundamentals:** Used for the initial universe filter (e.g., market capitalization, average volume).
- **News Catalyst:** Provides the baseline news headlines for NLP analysis.

### 2.2 Alternative Data for "Narrative Strength"

A high `Catalyst_Score` is derived from a coherent theme emerging from multiple data sources:

- **SEC Filings (via sec-api.io or similar):**
  - **Form 8-K:** Detects unscheduled material events (e.g., M&A, bankruptcy).
  - **Forms 3, 4, 5:** Identifies clusters of insider buying or selling.
- **Social Sentiment (via StockTwits, Reddit API):**
  - Monitors the *rate of change* of sentiment scores and mention volume.
- **Sector-Specific Catalysts (e.g., Biotech):**
  - Uses specialized databases to track clinical trial phases, PDUFA dates, etc.

## 3. Quantitative Scoring Engine: The Chart Clarity Score

The `Chart_Clarity_Score` is a composite, weighted average of seven distinct, quantifiable metrics designed to assess the quality and predictability of a pre-market consolidation. It is a sophisticated filter to ensure the agent only engages with the most orderly and high-probability setups.

### 3.1 The Seven Core Metrics

| Metric Name | Abbreviation | Category | Core Concept |
| :--- | :--- | :--- | :--- |
| **Range Integrity Score** | RIS | Price Action | How well price respects support/resistance boundaries. |
| **Price Action Rhythm Score** | PRS | Price Action | The orderliness and symmetry of price swings within the range. |
| **Volatility Character Score** | VCS | Price Action | The *nature* of volatility (constructive vs. erratic). |
| **Volume Profile Structure Score** | VPSS | Volume | The clarity and consensus shown in the volume-at-price distribution. |
| **Volume Trend & Confirmation Score** | VTCS | Volume | The dynamic behavior of volume over time during the consolidation. |
| **Order Flow Absorption Score** | OFAS | Order Flow | Strength of S/R based on absorption of aggressive orders. |
| **Cumulative Volume Delta Score** | CVDS | Order Flow | Net buying/selling pressure and its divergence from price. |

## 4. The ML-Powered Adaptive Ranking Loop

To prevent alpha decay, the system uses a post-market, closed-loop system that uses machine learning to refine the pre-market ranking algorithm. This is achieved with a **meta-labeling** framework.

- **Primary Model (e.g., XGBoost):** Predicts the *direction* of a potential trade (+1 for long, -1 for short) based on the full set of engineered features.
- **Secondary Model (e.g., Logistic Regression):** Predicts the *probability that the primary model is correct*. Its output is a confidence score (0.0 to 1.0) that is used to filter and rank the initial signals, and can be used for probabilistic position sizing.