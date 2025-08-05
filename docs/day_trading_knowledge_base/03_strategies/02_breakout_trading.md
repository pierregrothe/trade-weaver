# [STRATEGY: Breakout] Breakout Trading: Opening Range Breakout (ORB)

This document details a specific and powerful breakout strategy: the Opening Range Breakout (ORB), designed to exploit the predictable volatility spike and price discovery mechanism at the market open.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** The ORB is an event-driven strategy that trades the outcome of a predictable, daily liquidity event: the 9:30 AM EST market open.
- **[WHY]** The edge comes from exploiting the **forced price discovery** that resolves overnight order imbalances. A decisive break from the initial range (the "Opening Range") provides a high-probability signal of the day's institutional order flow direction. The strategy aims to ride this initial, powerful trend.
- **[RISK: Edge_Erosion]** The basic ORB edge is well-known and has been eroded by HFTs. A modern, profitable implementation requires strict **confirmation filters** (candle close, volume surge) to avoid frequent false breakouts and "whipsaws."

### [CONCEPT: Optimal_Parameters] 2. Optimal Implementation Parameters (NASDAQ 100, 5-min)

- **[PARAMETER: Range_Duration]** A **15-minute opening range (9:30-9:45 AM ET)** provides the most reliable support and resistance levels.
- **[PARAMETER: Entry_Trigger]** The optimal entry trigger is a **5-minute candle closing fully outside** the established 15-minute range.
- **[PARAMETER: Volume_Filter]** A **non-negotiable** entry filter: the volume of the 5-minute breakout candle must be **> 2.0 times the average volume** of the three 5-minute candles that formed the opening range.
- **[PARAMETER: Stop_Loss]** The optimal initial stop-loss is placed at a distance of **200% of the opening range width** from the entry point to allow the trade room to work.
- **[PARAMETER: Profit_Target]** The optimal exit is to **hold the position until the market close (EOC)**. This allows the strategy to capture the entirety of strong intraday trends, creating a positive profit skew.

### [CONCEPT: Performance_Analysis] 3. Quantitative Performance Analysis

- **Performance by Volatility Regime (VIX):**
  - **Low VIX (<20):** **Unprofitable.** Profit Factor: **< 1.0**. Lacks conviction for breakouts.
  - **Medium VIX (20-30):** **Favorable.** Profitable with positive expectancy.
  - **High VIX (>30):** **Optimal.** Fear drives powerful, sustained intraday trends. Profit Factor is expected to be **> 2.0**.

- **Performance by Prior Day's Trend (ADX on QQQ):**
  - **After Ranging Day (ADX < 25):** **Optimal.** Profit Factor: **> 1.9**. A breakout after consolidation (a "coiled spring") is more explosive.
  - **After Trending Day (ADX > 25):** **Unfavorable.** Profit Factor: **~1.1**. Higher risk of trend exhaustion.

- **[RULE: Time_Filter]** The ORB strategy module **must be disabled after 12:00 PM ET**.

### [CONCEPT: ADK_Implementation] 4. ADK Implementation Notes

- **[HOW]** A **hybrid, two-tiered architecture** is recommended.
    1. **[AGENT: LlmAgent] Strategic Layer:** An `OrbStrategyManager` agent runs once pre-market. It performs regime analysis (VIX, ADX) and catalyst screening. If conditions are favorable, it authorizes the strategy by passing a list of approved symbols to the tactical layer via `ToolContext.state`.
    2. **[TOOL: FunctionTool] Tactical Layer:** A deterministic `execute_orb_trade` `FunctionTool` receives the approved symbols from state. It then handles all high-frequency, mechanical logic intraday without any further LLM discretion.

[SOURCE_ID: ORB Strategy Quantitative Analysis]
