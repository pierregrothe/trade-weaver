# [STRATEGY: Mean_Reversion] Intraday Mean Reversion

This document details the Mean Reversion strategy, a counter-trend approach that profits from the statistical tendency of prices to revert to their historical average after an overextension.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** Mean reversion operates on the principle that price extremes are temporary and that prices will tend to return to a central value (the "mean"). The strategy involves buying assets that have fallen significantly and shorting assets that have risen significantly, betting on a "snap-back."
- **[WHY]** The edge is derived from market overreactions. Behavioral biases can cause prices to overshoot their intrinsic value. Mean reversion profits from the correction of these overreactions. It is most effective in ranging markets where there is no strong directional trend.
- **[RISK: Trend_Continuation]** The primary risk is "catching a falling knife" - shorting what appears to be an overextension that is actually the beginning of a new, strong uptrend. A mean reversion trader can suffer large losses if they fight a persistent trend, making risk management and regime filtering critical.

### [CONCEPT: Optimal_Parameters] 2. Optimal Implementation Parameters

- **[REGIME: Ranging_Market]** This strategy is most effective in **range-bound or oscillating markets**. The agent must use a regime filter, such as an **ADX < 25**, as a mandatory prerequisite for enabling this strategy.
- **[INDICATOR: Bollinger_Bands]** Bollinger Bands are the primary tool for identifying statistical extremes. They consist of a moving average (the mean) and bands plotted at a set number of standard deviations (typically 2) above and below it.
- **[INDICATOR: Bollinger_Band_Width]** The distance between the upper and lower bands can be used as a volatility filter. A mean reversion strategy is more reliable when the bands are wide (high volatility), as this indicates more room for price to revert. When bands are very narrow (a "squeeze"), it signals low volatility and can precede a strong breakout, which is dangerous for this strategy.
- **[INDICATOR: RSI]** The Relative Strength Index (RSI) is used to confirm overbought/oversold conditions. A reading > 70 indicates overbought, and < 30 indicates oversold.
- **[SIGNAL: Confluence]** The highest-probability signals come from confluence. A long entry is triggered when the price touches the lower Bollinger Band **AND** the RSI is oversold (<30). A short entry is triggered when the price touches the upper Bollinger Band **AND** the RSI is overbought (>70).

### [CONCEPT: Performance_Profile] 3. Quantitative Performance Profile

- **Win Rate:** Mean reversion strategies typically have a high win rate (often 70-85%) because prices spend more time in ranges than in strong trends.
- **Risk/Reward:** The trade-off for a high win rate is a lower average profit per trade compared to momentum strategies. The strategy relies on a large number of small, consistent wins.
- **Risk Management:** Because a single strong trend can erase many small wins, strict risk management is non-negotiable. Stop-losses must be placed to cap the risk if the expected reversion does not occur.
- **Profit Target:** The most common and logical profit target for a mean reversion trade is the middle Bollinger Band (the moving average), as this represents a return to the mean.

[SOURCE_ID: Intraday Mean Reversion Strategy Analysis]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]
[SOURCE_ID: A Quantitative Framework for Algorithmic Day Trading: Regime Analysis, Pre-Market Evaluation, and Strategy Implementation]