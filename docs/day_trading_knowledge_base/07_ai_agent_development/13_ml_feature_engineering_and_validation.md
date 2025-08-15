# [CONCEPT: ML_Validation] ML Feature Engineering and Validation for Intraday Trading

This document provides a quantitative guide to engineering predictive features for intraday trading strategies and, more importantly, the rigorous validation techniques required to prevent data leakage and backtest overfitting.

### [PRINCIPLE: Feature_Engineering] 1. Feature Engineering for Opening Range Breakout (ORB) Strategies

Effective feature engineering moves beyond simple price levels to quantify the microstructural signals that determine breakout viability.

- **[FEATURE: Relative_Volume_RVOL]** The paramount feature. It identifies "Stocks in Play" and confirms institutional conviction. It should be calculated for very short, early-session timeframes (e.g., the first 1-5 minutes) and normalized for time of day.
- **[FEATURE: Gap_Percentage]** The size and direction of the pre-market gap provide a crucial context, signaling the initial supply/demand imbalance from overnight news.
- **[FEATURE: Bid-Ask_Spread_Dynamics]** The spread at the moment of breakout is a real-time gauge of liquidity and risk. A breakout that clears a wide spread with conviction is more robust than one that nudges the edge of a tight spread.
- **[FEATURE: Pre-Market_VWAP_Distance]** The distance between the opening price and the pre-market VWAP can signal whether a move is an extension from or a reversion to the pre-market "fair value."
- **[FEATURE: Sector_Relative_Strength]** A macro-contextual filter that ensures the breakout is supported by a broader market narrative, not just idiosyncratic noise.

### [PRINCIPLE: Data_Labeling] 2. Economically Meaningful Labeling Schemas

How a trade outcome is labeled is critical for training a useful model. Simple fixed-horizon labels are often flawed.

- **[TECHNIQUE: Triple-Barrier_Method]** This is the superior method for financial machine learning. It defines three barriers for each observation:
    1.  **Upper Barrier (Profit-Taking)**
    2.  **Lower Barrier (Stop-Loss)**
    3.  **Vertical Barrier (Time Limit)**
- **[RATIONALE]** This method is volatility-adaptive and directly links the label to a realistic trading outcome (hit profit target, hit stop-loss, or timed out), making the model's predictions economically meaningful.
- **[TECHNIQUE: Meta-Labeling]** A powerful extension that separates the **side** of the bet from the **size** of the bet. A primary model (e.g., a simple technical rule) determines the direction (long/short). A secondary ML model then learns to predict the *probability that the primary model is correct*, which can be used for sophisticated position sizing.

### [PRINCIPLE: Validation] 3. The Imperative of Unbiased Out-of-Sample Performance

Financial time series data is non-stationary and exhibits strong serial correlation. Naive validation techniques lead to data leakage and catastrophic failures in live trading.

- **[RISK: Data_Leakage]** Occurs when information from the test set inadvertently contaminates the training set. This is the primary cause of "backtest overfitting."
- **[SOLUTION: Purged_K-Fold_Cross-Validation]** A modified K-Fold CV that incorporates:
    - **Purging:** Removing training set observations that overlap with the formation period of labels in the test set.
    - **Embargo:** Introducing a time gap between the training and testing sets to prevent future information from leaking backward.
- **[SOLUTION: Walk-Forward_Optimization_WFO]** The gold standard for financial backtesting. WFO simulates real-world adaptation by repeatedly optimizing the model on a rolling "in-sample" window and testing it on the next "out-of-sample" window. This is the only way to get a realistic estimate of a learning agent's performance.

### [CONCEPT: Probabilistic_Calibration] 4. From Predictions to Profits: Probability Calibration

For quantitative trading, a model's raw probability outputs are often uncalibrated and cannot be trusted for decision-making. Calibration transforms these raw outputs into reliable, trustworthy probabilities.

- **[WHY]** A model that says there is an 80% chance of profit should be correct approximately 80% of the time. Without this, risk management and position sizing are fundamentally flawed.
- **[METRICS: Brier_Score_and_Skill_Score]**
    - **Brier Score:** The primary measure of probabilistic forecast accuracy (a lower score is better).
    - **Brier Skill Score (BSS):** The crucial metric for acceptance testing. It measures the model's improvement over a naive baseline. A **BSS > 0** is the minimum acceptance criterion, as it indicates the model provides value beyond a simple historical average.
- **[APPLICATION: Prob-Aware_Sizing]** Calibrated probabilities are a direct input for advanced position sizing models like the **Kelly Criterion**, allowing the system to dynamically size trades based on the model's confidence, taking more risk on high-probability setups and less on marginal ones.
