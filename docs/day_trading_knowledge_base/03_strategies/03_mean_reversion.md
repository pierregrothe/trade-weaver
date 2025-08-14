# [STRATEGY: Mean_Reversion] Mean Reversion Trading

This document details the Mean Reversion strategy, a counter-trend approach that profits from the statistical tendency of prices to revert to their historical average.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** Mean reversion operates on the principle that price extremes are temporary and that prices will tend to return to a central value (the "mean"). The strategy involves buying assets that have fallen significantly and shorting assets that have risen significantly, betting on a "snap-back."
- **[WHY]** The edge is derived from market overreactions. Behavioral biases can cause prices to overshoot their intrinsic value. Mean reversion profits from the correction of these overreactions.
- **[RISK: Trend_Continuation]** The primary risk is that what appears to be an overextension is actually the beginning of a new, strong trend. A mean reversion trader can suffer large losses if they fight a persistent trend, making risk management critical.

### [CONCEPT: Optimal_Parameters] 2. Optimal Implementation Parameters

- **[REGIME: Ranging_Market]** This strategy is most effective in **range-bound or oscillating markets** with no strong directional trend (i.e., low ADX).
- **[INDICATOR: Bollinger_Bands]** Bollinger Bands are a primary tool. They consist of a moving average (the mean) and bands plotted at a set number of standard deviations (typically 2) above and below it. A price touching or piercing the outer bands signals a statistical extreme.
- **[INDICATOR: RSI]** The Relative Strength Index (RSI) is used to confirm overbought/oversold conditions. A reading > 70 indicates overbought, and < 30 indicates oversold.
- **[SIGNAL: Confluence]** The highest-probability signals come from confluence. A long entry is triggered when the price touches the lower Bollinger Band **AND** the RSI is oversold (<30). A short entry is triggered when the price touches the upper Bollinger Band **AND** the RSI is overbought (>70).

### [CONCEPT: Performance_Analysis] 3. Quantitative Performance Analysis

- **Win Rate:** Mean reversion strategies typically have a high win rate (often 70-85%) because prices spend more time in ranges than in strong trends. However, the average profit per trade is usually smaller than in momentum strategies.
- **Risk Management:** Because a single strong trend can erase many small wins, strict risk management is non-negotiable. Stop-losses must be placed to cap the risk if the expected reversion does not occur.
- **Profit Target:** The most common and logical profit target for a mean reversion trade is the middle Bollinger Band (the moving average), as this represents a return to the mean.

[SOURCE_ID: Intraday Mean Reversion Strategy Analysis]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]
[SOURCE_ID: A Quantitative Framework for Algorithmic Day Trading: Regime Analysis, Pre-Market Evaluation, and Strategy Implementation]
