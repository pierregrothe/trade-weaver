# [CONCEPT: Trade_Selection] Advanced Trade Selection and Sizing Algorithm

This document details the quantitative algorithm for selecting and sizing an optimal portfolio of trades from a larger watchlist. This process moves beyond simply picking the highest-scored setups; it actively manages and diversifies correlated risk at the point of trade inception using Hierarchical Risk Parity (HRP).

### [PRINCIPLE: Alpha_vs_Risk] The Core Problem: Alpha vs. Correlated Risk

An AI's alpha model may generate numerous high-conviction trade signals (e.g., 10 "A+" setups). However, if many of these signals are in the same sector (e.g., semiconductors) and driven by the same catalyst, executing all of them would create a single, massive, undiversified bet on that one factor. This algorithm solves that problem by balancing the alpha signal with a quantitative measure of diversification.

### [CONCEPT: Selection_Algorithm] The Four-Step Selection & Sizing Algorithm

The agent must execute the following sequential process:

#### [STEP: 1] Step 1: Initial Scoring & Risk Filtering

- **[TASK: Alpha_Scoring]** The process begins with the watchlist of potential trade setups, each assigned an "alpha score" by the agent's signal generation model (e.g., the `overall_score` from the pre-market analysis).
- **[TASK: Risk_Filtering]** All candidates are passed through a risk filter. Any stock exhibiting extreme characteristics is **immediately discarded**, regardless of its alpha score.
  - **[RULE: Volatility_Filter]** Discard if `ATR (14-day) > 5% of Current_Price`.
  - **[RULE: Liquidity_Filter]** Discard if `Average Dollar Volume (30-day) < $20,000,000`.

#### [STEP: 2] Step 2: Hierarchical Clustering & Diversification Analysis

- **[TASK: Dynamic_Correlation]** The agent computes a dynamic, intraday correlation matrix for the remaining candidates using high-frequency (e.g., 5-minute) return data.
- **[TECHNIQUE: HRP_Clustering]** This correlation matrix is fed into the **Hierarchical Risk Parity (HRP)** clustering algorithm. HRP is a machine learning technique that groups assets based on their similarity. The output is a dendrogram (tree structure) that mathematically groups the candidates based on their correlation. Highly correlated stocks (e.g., five semiconductor stocks) will form a single, tight cluster.

#### [STEP: 3] Step 3: Cluster-Based Trade Selection

- **[PRINCIPLE: Maximize_Diversification]** The core of the selection logic is to maximize diversification by picking trades from different correlation clusters.
- **[TASK: Cluster_Traversal]** The algorithm's goal is to select `N` trades (e.g., `N=4`). It traverses the dendrogram and selects the **single highest alpha-scoring candidate** from each of the `N` most distinct, high-level clusters.
- **[OUTCOME: Diversified_Selection]** This method ensures that the selected portfolio is, by construction, diversified across the main drivers of risk present in the watchlist. It directly prevents the agent from loading up on multiple, highly correlated assets from the same group.

#### [STEP: 4] Step 4: Risk Parity Position Sizing

- **[PRINCIPLE: Equal_Risk_Contribution]** The selected trades are not sized using the 1% rule individually, as this ignores their inter-correlations. Instead, the final portfolio is sized according to the **Risk Parity** principle.
- **[TASK: Optimization]** The objective of risk parity is to size positions such that each asset contributes an **equal amount of risk** to the total portfolio volatility. An optimizer solves for the set of capital weights that achieves this goal, subject to the constraint that total portfolio risk does not violate higher-level rules.
- **[OUTCOME: Risk_Balanced_Portfolio]** This process naturally allocates less capital to assets that are more volatile or more highly correlated with the rest of the selected portfolio, resulting in a truly risk-balanced final allocation.

### [CONCEPT: ADK_Implementation] ADK Implementation Notes

- **[HOW]** This entire process can be encapsulated in a single `FunctionTool` called `select_and_size_portfolio`. This tool would take the watchlist as input and return a dictionary of tickers and their corresponding position sizes.
- **[ORCHESTRATION]** The main agent would call this tool after the pre-market scanning is complete. The output of this tool would then be used to place the opening trades for the day.

[SOURCE_ID: Intraday Portfolio Risk Management, Section 4 & 5]
[SOURCE_ID: Hierarchical Risk Parity for Portfolio Selection]