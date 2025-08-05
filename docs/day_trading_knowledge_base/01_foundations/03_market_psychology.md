# [CONCEPT: Market_Psychology] Market Psychology and AI Countermeasures

Financial markets are a reflection of mass human psychology. An AI agent, while emotionless, must be programmed with explicit countermeasures to prevent it from replicating the destructive behavioral patterns that arise from human cognitive biases.

### [BIAS: Revenge_Trading] Revenge Trading

- **[BEHAVIOR: Definition]** The emotional urge to immediately "win back" money after a loss, leading to impulsive, oversized, and low-probability trades. It is a primary cause of catastrophic account losses.
- **[SIGNATURE: Detection]** A rapid sequence of new trades initiated immediately after a trade is closed for a significant loss, often with increased position size.
- **[AI_COUNTERMEASURE: Daily_Loss_Circuit_Breaker]** A non-negotiable, system-wide kill switch.
  - **[PARAMETER: MAX_DAILY_LOSS_PERCENT=0.06]** Hard-coded system parameter for a maximum daily loss of 6% of the session's starting equity.
  - **[RULE: System_Halt]** `ON_TRADE_CLOSE: IF daily_realized_pnl <= -(account_equity_start_of_day * 0.06) THEN execute_flatten_all_positions() AND set_system_state('HALT_TRADING_FOR_DAY')`.

### [BIAS: FOMO] Fear of Missing Out (FOMO)

- **[BEHAVIOR: Definition]** Chasing a stock after a large, rapid price move has already occurred, resulting in a poor entry price with an unfavorable risk-to-reward profile.
- **[SIGNATURE: Detection]** The price of an asset is trading at a statistically significant deviation from its short-term mean (e.g., more than `1.5 * ATR` above its 20-period EMA).
- **[AI_COUNTERMEASURE: Price_Extension_Filter]** A rule preventing the agent from entering trades when the price is statistically overextended.
  - **[RULE: FOMO_Filter_Long]** `ON_LONG_ENTRY_SIGNAL: IF entry_price > (ema(20) + (1.5 * atr(14))) THEN REJECT_SIGNAL`.
  - **[RULE: FOMO_Filter_Short]** `ON_SHORT_ENTRY_SIGNAL: IF entry_price < (ema(20) - (1.5 * atr(14))) THEN REJECT_SIGNAL`.

### [BIAS: Complacency_Euphoria] Complacency / Euphoria

- **[BEHAVIOR: Definition]** After a long winning streak, human traders become overconfident. They may start taking larger risks, ignoring their rules, and believing they cannot lose, which often precedes a large drawdown.
- **[SIGNATURE: Detection]** A consecutive streak of a predefined number of winning trades (e.g., 8 or more) or a significant increase in the account's profit factor over a short period.
- **[AI_COUNTERMEASURE: Risk_Reduction_Protocol]** An intelligent agent should do the opposite of an emotional human. Instead of increasing risk during a winning streak, it should protect its gains.
  - **[RULE: Winning_Streak_Risk_Reduction]** `ON_TRADE_CLOSE: IF winning_streak_count >= 8 THEN reduce_max_risk_per_trade_to(0.005)`. The risk parameter is reset to 1% only after the streak is broken by a losing trade.

### [BIAS: Confirmation_Bias] Confirmation Bias

- **[BEHAVIOR: Definition]** The tendency to seek out and interpret information that confirms one's pre-existing beliefs or trade thesis, while ignoring evidence that contradicts it. For an AI, this could manifest as a model that overweights data confirming a pattern it has initially identified.
- **[SIGNATURE: Detection]** A strategy that relies on multiple, highly correlated indicators (e.g., three different types of momentum oscillators) will suffer from confirmation bias. The signals will appear strong because they are essentially measuring the same thing.
- **[AI_COUNTERMEASURE: Indicator_Decoupling]** The agent's strategies must be built using a diverse set of indicators that measure different aspects of the market (e.g., combining a **trend** indicator, a **momentum** indicator, and a **volume** indicator). The system should flag strategies where more than 50% of the inputs are from the same category (e.g., all momentum) for review.

[SOURCE_ID: Day Trading AI Agent Research, Part I, Section 1.1]
[SOURCE_ID: AI Day Trading Blueprint, Section 1.2]
