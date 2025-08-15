# [STRATEGY: Momentum] Intraday Momentum Trading

This document provides a deep dive into the Intraday Momentum strategy, detailing its statistical rationale, optimal parameters, quantified performance, and implementation architecture.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** Momentum trading seeks to capitalize on the continuation of an established price trend, operating under the philosophy of **"buy high and sell higher"** or **"short low and cover lower."**
- **[WHY]** The inefficiency arises from several behavioral phenomena:
    1. **[BIAS: Investor_Herding]** The tendency of individuals to mimic the actions of a larger group. A strong directional move attracts "fear of missing out" (FOMO) buyers, which amplifies the initial move and creates a self-sustaining trend.
    2. **[BIAS: Underreaction]** Markets do not instantaneously incorporate all new information. The staggered reaction of different market participants to a catalyst (like an earnings report) causes a price to "drift" in the direction of the news over time, creating a persistent, tradable trend.
- **[RISK: Momentum_Crash]** The strategy's reliance on these psychological factors is also its greatest vulnerability. During periods of extreme market stress (High VIX), these biases can violently reverse, leading to a "momentum crash" where the strategy incurs significant losses.

### [CONCEPT: Optimal_Parameters] 2. Optimal Implementation Parameters (5-min, NASDAQ 100)

- **[UNIVERSE]** The NASDAQ 100 is an ideal universe due to its high liquidity, volatility, and constant news flow. The best candidates within the index are those with high Beta (relative to QQQ) and high ATR as a percentage of price.
- **[INDICATOR: EMA_Crossover]** The primary signal is a **13-period / 48-period EMA crossover**, which provides a well-tested balance between responsiveness and noise filtration.
- **[INDICATOR: RSI_Filter]** The Relative Strength Index (RSI) is repurposed as a momentum filter. Instead of just identifying overbought/oversold levels, the **50-level** is key. In a strong uptrend, RSI should hold above 50-60. Entries are often taken when RSI dips toward 40 during a pullback and then recovers, confirming sustained bullish momentum. A long entry requires `RSI(9) > 55`; a short entry requires `RSI(9) < 45`.
- **[INDICATOR: MACD_Filter]** A faster **MACD(8, 17, 9)** is used for trend confirmation. A long entry requires a bullish crossover (`MACD_Line > MACD_Signal_Line`) with both lines preferably above the zero line, indicating positive momentum.
- **[INDICATOR: ADX_Filter]** An **ADX reading > 25** should be a precondition for enabling the momentum strategy module, confirming the market is in a trending regime.
- **[INDICATOR: Risk_Management]** Stop-loss and take-profit levels are dynamically set based on the **14-period ATR**, enforcing a strict **2:1 Reward/Risk ratio**.

### [CONCEPT: Chart_Patterns] 3. Chart Pattern Continuation Signals

- **[PATTERN: Bull_Flag]** A primary pattern for momentum traders. After a strong, high-volume upward move (the "flagpole"), the stock consolidates in a tight, downward-sloping channel on low volume (the "flag"). A breakout from the top of this flag on a surge of volume is a high-probability entry signal for the next leg of the trend.
- **[PATTERN: Higher_Highs_Lows]** The agent should confirm the basic structure of an uptrend: a sequence of higher highs and higher lows on the intraday chart.

### [CONCEPT: Performance_Analysis] 4. Quantitative Performance Analysis

- **Performance by Volatility Regime (VIX):**
  - **Low VIX (<20):** **Optimal.** Profit Factor: **1.98**. Sharpe Ratio: **1.85**.
  - **Medium VIX (20-30):** **Good.** Profit Factor: **1.51**. Sharpe Ratio: **1.22**.
  - **High VIX (>30):** **Unprofitable.** Profit Factor: **0.87**. The strategy **must be disabled** in this regime due to the high risk of sharp reversals and momentum crashes.

- **Performance by Trend Regime (ADX on QQQ):**
  - **Ranging Market (ADX < 25):** **Marginal.** Profit Factor: **1.15**. Prone to "whipsaws." The ADX filter is designed to prevent trading in this state.
  - **Trending Market (ADX > 25):** **Highly Profitable.** Profit Factor: **1.89**. The strategy's ideal operational state.

- **Performance by Time of Day (ET):**
  - **Opening Hour (9:30-10:30):** **Strong.** Profit Factor: **1.85**.
  - **Midday Lull (10:30-15:00):** **Break-even.** Profit Factor: **1.08**.
  - **Closing Hour (15:00-16:00):** **Strong.** Profit Factor: **1.79**.

[SOURCE_ID: Intraday Momentum Strategy Analysis]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]
[SOURCE_ID: A Quantitative Framework for Algorithmic Day Trading: Regime Analysis, Pre-Market Evaluation, and Strategy Implementation]