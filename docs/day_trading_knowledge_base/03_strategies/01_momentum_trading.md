# [STRATEGY: Momentum] Momentum Trading

This document provides a deep dive into the Intraday Momentum strategy, detailing its statistical rationale, optimal parameters, quantified performance, and implementation architecture.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** Momentum trading seeks to capitalize on the continuation of an established price trend, operating under the philosophy of **"buy high and sell higher"** or **"short low and cover lower."**
- **[WHY]** The inefficiency arises from several behavioral phenomena:
    1. **[BIAS: Investor_Herding]** The tendency of individuals to mimic the actions of a larger group. A strong directional move attracts "fear of missing out" (FOMO) buyers, which amplifies the initial move and creates a self-sustaining trend.
    2. **[BIAS: Underreaction]** Markets do not instantaneously incorporate all new information. The staggered reaction of different market participants to a catalyst (like an earnings report) causes a price to "drift" in the direction of the news over time, creating a persistent, tradable trend.
    3. **[BIAS: Confirmation_Bias]** Investors in a profitable trend are psychologically predisposed to favor information that confirms their decision, causing them to hold positions longer and contributing to the trend's persistence.
- **[RISK: Momentum_Crash]** The strategy's reliance on these psychological factors is also its greatest vulnerability. During periods of extreme market stress (High VIX), these biases can violently reverse, leading to a "momentum crash" where the strategy incurs significant losses.

### [CONCEPT: Optimal_Parameters] 2. Optimal Implementation Parameters (5-min, NASDAQ 100)

- **[UNIVERSE]** The NASDAQ 100 is an ideal universe due to its high liquidity, volatility, and constant news flow. The best candidates within the index are those with high Beta (relative to QQQ) and high ATR as a percentage of price.
- **[INDICATOR: EMA_Crossover]** The primary signal is a **13-period / 48-period EMA crossover**, which provides the best-backtested balance between responsiveness and noise filtration.
- **[INDICATOR: RSI_Filter]** A **9-period RSI** is used for momentum confirmation. A long entry requires `RSI(9) > 55`; a short entry requires `RSI(9) < 45`.
- **[INDICATOR: MACD_Filter]** A faster **MACD(8, 17, 9)** is used for trend confirmation. A long entry requires a bullish crossover (`MACD_Line > MACD_Signal_Line`).
- **[INDICATOR: Risk_Management]** Stop-loss and take-profit levels are dynamically set based on the **14-period ATR**, enforcing a strict **2:1 Reward/Risk ratio**.

### [CONCEPT: Performance_Analysis] 3. Quantitative Performance Analysis

- **Performance by Volatility Regime (VIX):**
  - **Low VIX (<20):** **Optimal.** Profit Factor: **1.98**. Sharpe Ratio: **1.85**.
  - **Medium VIX (20-30):** **Good.** Profit Factor: **1.51**. Sharpe Ratio: **1.22**.
  - **High VIX (>30):** **Unprofitable.** Profit Factor: **0.87**. The strategy **must be disabled** in this regime.

- **Performance by Trend Regime (ADX on QQQ):**
  - **Ranging Market (ADX < 25):** **Marginal.** Profit Factor: **1.15**. Prone to "whipsaws."
  - **Trending Market (ADX > 25):** **Highly Profitable.** Profit Factor: **1.89**. The strategy's ideal operational state.

- **Performance by Time of Day (ET):**
  - **Opening Hour (9:30-10:30):** **Strong.** Profit Factor: **1.85**.
  - **Midday Lull (10:30-15:00):** **Break-even.** Profit Factor: **1.08**.
  - **Closing Hour (15:00-16:00):** **Strong.** Profit Factor: **1.79**.

### [CONCEPT: ADK_Implementation] 4. ADK Implementation Notes

- **[HOW]** The optimal architecture is a **hybrid, supervisory model**.
    1. **[TOOL: FunctionTool] The Execution Agent:** The core trading logic (indicator calculation, entry/exit rules) should be encapsulated in a deterministic, high-speed Python function and exposed to the agent as a **`FunctionTool`** (e.g., `execute_momentum_trade`).
    2. **[AGENT: LlmAgent] The Supervisory Agent:** A supervisory `LlmAgent` is responsible for strategic oversight. Its role is to:
        - Call a `MarketRegimeTool` to get the current VIX, ADX, and time.
        - Based on the performance data above, decide *if* and *when* to authorize the `execute_momentum_trade` tool.
        - Its instruction prompt would contain the logic: `"You are a risk manager. Only authorize the momentum tool if VIX < 30 and ADX > 25 during the opening or closing hours."`

[SOURCE_ID: Intraday Momentum Strategy Analysis]
