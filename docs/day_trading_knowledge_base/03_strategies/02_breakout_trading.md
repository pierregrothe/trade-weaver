# [STRATEGY: Breakout] Breakout Trading: Opening Range Breakout (ORB)

This document details a specific and powerful breakout strategy: the Opening Range Breakout (ORB), designed to exploit the predictable volatility spike and price discovery mechanism at the market open.

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** The ORB is an event-driven strategy that trades the outcome of a predictable, daily liquidity event: the 9:30 AM EST market open.
- **[WHY]** The edge comes from exploiting the **forced price discovery** that resolves overnight order imbalances. A decisive break from the initial range (the "Opening Range") provides a high-probability signal of the day's institutional order flow direction. Statistical studies have shown that on highly volatile days, the market open frequently occurs near the eventual high or low of the day, meaning the initial move often sets the day's trend.
- **[RISK: Edge_Erosion]** The basic ORB edge is well-known and has been eroded by HFTs. A modern, profitable implementation requires strict **confirmation filters** (e.g., candle close, volume surge, catalyst) to avoid frequent false breakouts and "whipsaws."

### [CONCEPT: Optimal_Parameters] 2. Optimal Implementation Parameters (NASDAQ 100, 5-min)

- **[PARAMETER: Range_Duration]** The choice of range duration is a trade-off. Shorter ranges (5-15 min) offer quicker entries but more false signals. Longer ranges (30-60 min) provide more reliable levels but later entries. Backtesting on SPX 0DTE options shows a 60-minute range significantly outperforms shorter timeframes.
- **[PARAMETER: Entry_Trigger]** The optimal entry trigger is a **full candle closing outside** the established opening range, not just a wick piercing it. This helps filter out fakeouts.
- **[PARAMETER: Volume_Filter]** A **non-negotiable** entry filter: the volume of the breakout candle must be substantially higher than the average volume of the preceding candles (e.g., `> 2.0x`). This confirms institutional conviction.
- **[PARAMETER: Stop_Loss]** The initial stop-loss is placed at a logical invalidation point, typically on the opposite side of the opening range. This defines a clear and contained risk for the trade.
- **[PARAMETER: Profit_Target]** Targets can be set using a fixed risk/reward multiple (e.g., 2:1), at key technical levels (pivots, prior day's high/low), or by holding until the End-of-Close (EOC) to capture the full day's trend.

### [CONCEPT: Critical_Filters] 3. Critical Filters for Success

- **[FILTER: Stocks_in_Play]** The strategy should be focused on "stocks in play"—those with a clear pre-market catalyst (earnings, news) and high relative volume. A breakout in a stock with no news is less likely to have follow-through.
- **[FILTER: Broad_Market_Context]** The agent must consider the broad market trend. An upside breakout has a higher probability of success if the overall market (e.g., SPY, QQQ) is also trending up.

### [CONCEPT: Performance_Analysis] 4. Quantitative Performance Analysis

Unfiltered ORB strategies are often unprofitable. The edge is derived from intelligent filtering. Backtests show that filtering for the daily trend direction or using longer timeframes dramatically improves performance.

| ORB Timeframe | Instrument | Strategy Details | Win Rate | Profit Factor | Source(s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5-min | S&P 500 Futures | Simple Breakout (Long) | Low | < 1.0 | Quantified Strategies |
| 60-min | SPX (0DTE Options) | Combined Long/Short | 88.8% | 1.59 | Option Alpha |
| 1-min | Nasdaq Futures | With Daily Trend Filter | 65% | 2.0 | Quantified Strategies |

- **Performance by Volatility Regime (VIX):**
  - **Low VIX (<20):** **Unprofitable.** Lacks conviction for breakouts.
  - **Medium VIX (20-30):** **Favorable.** Profitable with positive expectancy.
  - **High VIX (>30):** **Optimal.** Fear drives powerful, sustained intraday trends.

### [CONCEPT: ADK_Implementation] 5. ADK Implementation Notes

- **[HOW]** A **hybrid, two-tiered architecture** is recommended.
    1. **[AGENT: LlmAgent] Strategic Layer:** An `OrbStrategyManager` agent runs once pre-market. It performs regime analysis (VIX, ADX) and catalyst screening. If conditions are favorable, it authorizes the strategy by passing a list of approved symbols to the tactical layer via `ToolContext.state`.
    2. **[TOOL: FunctionTool] Tactical Layer:** A deterministic `execute_orb_trade` `FunctionTool` receives the approved symbols from state. It then handles all high-frequency, mechanical logic intraday without any further LLM discretion, including:
        - Defining the opening range high/low.
        - Monitoring for a candle close outside the range.
        - Checking for the volume spike confirmation.
        - Executing the bracket order with a pre-defined stop-loss and profit target.

[SOURCE_ID: ORB Strategy Quantitative Analysis]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]
[SOURCE_ID: A Quantitative Framework for Algorithmic Day Trading: Regime Analysis, Pre-Market Evaluation, and Strategy Implementation]
