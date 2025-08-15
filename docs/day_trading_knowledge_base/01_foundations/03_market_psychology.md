# [CONCEPT: Market_Psychology] Market Psychology and AI Countermeasures

Financial markets are a reflection of mass human psychology. An AI agent, while emotionless, must be programmed with explicit, quantitative countermeasures to prevent it from replicating the destructive behavioral patterns that arise from human cognitive biases.

### [THEORY: Prospect_Theory] Prospect Theory: The Root of Trading Biases

Prospect Theory, developed by Kahneman and Tversky, is a cornerstone of behavioral finance that explains why traders often behave irrationally. Its core tenets are:

- **[CONCEPT: Loss_Aversion]** The pain of a loss is psychologically about twice as powerful as the pleasure of an equivalent gain. This creates an asymmetric response to risk.
- **[CONCEPT: Reference_Dependence]** People evaluate outcomes not in absolute terms, but as gains or losses relative to a reference point (typically the entry price).

This framework leads to predictable biases. In the domain of gains, traders become risk-averse to lock in a sure profit. In the domain of losses, they become risk-seeking to avoid the pain of realizing a loss. An AI does not have these emotional responses; its goal is to maximize expected value based on its programming, regardless of the path taken.

--- 

### [BIAS: Disposition_Effect] The Disposition Effect

- **[BEHAVIOR: Definition]** The direct result of Prospect Theory. It is the tendency to sell winning assets too early ("risk-averse in the domain of gains") while holding on to losing assets for too long ("risk-seeking in the domain of losses").
- **[SIGNATURE: Detection]** A portfolio analysis showing that the average holding time for losing trades is significantly longer than the average holding time for winning trades.
- **[AI_COUNTERMEASURE: Rule-Based_Exits]** The AI is inherently immune to this bias. Its exit decisions are based on a pre-defined, emotionless ruleset (e.g., a trailing stop-loss is hit, a profit target is reached, or a time-stop is triggered), not on the relationship between the current price and the entry price.

### [BIAS: Revenge_Trading] Revenge Trading

- **[BEHAVIOR: Definition]** The emotional urge to immediately "win back" money after a loss, leading to impulsive, oversized, and low-probability trades.
- **[SIGNATURE: Detection]** A rapid sequence of new trades initiated in the same instrument immediately after a trade is closed for a significant loss, often with increased position size.
- **[AI_COUNTERMEASURE: Cool-Down_Protocol]** A targeted, time-based circuit breaker.
    - **[RULE: Cool-Down]** `ON_TRADE_CLOSE: IF trade.pnl < 0 AND abs(trade.pnl) > (2 * portfolio.avg_loss_last_20_trades) THEN disable_trading_in_asset(trade.ticker) FOR 30_minutes.`

### [BIAS: FOMO] Fear of Missing Out (FOMO)

- **[BEHAVIOR: Definition]** Chasing a stock after a large, rapid price move has already occurred, resulting in a poor entry price with an unfavorable risk-to-reward profile.
- **[SIGNATURE: Detection]** A price move that is both statistically overextended and occurring on waning volume, indicating the initial burst of institutional interest has passed.
- **[AI_COUNTERMEASURE: Price_Extension_and_Volume_Filter]** A rule preventing the agent from entering trades that are statistically overextended on low conviction.
    - **[RULE: FOMO_Filter_Long]** `ON_LONG_ENTRY_SIGNAL: IF (entry_price > (ema(20) + (1.5 * atr(14)))) AND (volume < volume_ma(20)) THEN REJECT_SIGNAL(reason="FOMO_CHASE_LOW_CONVICTION")`

### [BIAS: Complacency_Euphoria] Complacency / Euphoria

- **[BEHAVIOR: Definition]** After a long winning streak, human traders become overconfident, leading them to take larger risks and ignore their rules, which often precedes a large drawdown.
- **[SIGNATURE: Detection]** A statistically significant and rapid increase in the portfolio's short-term performance metrics.
- **[AI_COUNTERMEASURE: Dynamic_Risk_Reduction]** An intelligent agent does the opposite of an emotional human. Instead of increasing risk during a winning streak, it protects its gains.
    - **[RULE: Sharpe_Ratio_Spike]** `ON_TRADE_CLOSE: IF sharpe_ratio(last_20_trades) > 2.5 THEN reduce_max_risk_per_trade_to(0.005)`. The risk parameter is reset only after the Sharpe ratio normalizes.

### [BIAS: Anchoring_Bias] Anchoring Bias

- **[BEHAVIOR: Definition]** The tendency to rely too heavily on an initial piece of information, such as the trade's entry price, when making subsequent decisions.
- **[SIGNATURE: Detection]** Using a static entry price as the sole reference point for stop-loss or take-profit placement, ignoring new information and evolving market conditions.
- **[AI_COUNTERMEASURE: Dynamic_Reference_Points]** The AI avoids anchoring by using dynamic reference points for its decisions. For example, a trailing stop-loss is anchored to the `highest_price_since_entry`, not the `entry_price`. This ensures decisions are based on the current market reality, not on past events.

[SOURCE_ID: Day Trading AI Agent Research, Part I, Section 1.1]
[SOURCE_ID: AI Day Trading Blueprint, Section 1.2]
[SOURCE_ID: Prospect Theory and Behavioral Finance in Trading]
[SOURCE_ID: Disposition Effect and Anchoring Bias in Day Trading]