# [STRATEGY: Mid_Day_Mean_Reversion] Mid-Day Mean Reversion

This document details a quantitative strategy designed to exploit the unique microstructural characteristics of the U.S. equity mid-day session (typically 11:00 AM - 2:30 PM ET).

### [PRINCIPLE: Statistical_Edge] 1. Statistical Edge and Rationale

- **[WHAT]** The strategy is based on the principle of mean reversion, which posits that asset prices, after experiencing temporary extensions, tend to revert to their historical average. The "mean" in this context is the Volume-Weighted Average Price (VWAP).
- **[WHY]** The mid-day session is a distinct market regime where this strategy is particularly effective. The large, directional institutional flows that dominate the open and close are absent. The session is characterized by:
    - **Low and Stable Volume:** The "U-shaped" intraday volume profile is at its trough.
    - **Reduced Volatility:** Price action is more constrained and choppy.
    - **Dominance of Algorithmic Market-Making:** The participant ecology shifts to HFTs providing liquidity, which enforces range-bound, mean-reverting behavior.
- **[RISK: The_Chop]** The primary risk is not a strong trend, but "chop" - directionless, random price action. A filter is required to differentiate between orderly, reversible pullbacks and unprofitable noise.

### [CONCEPT: The_Dual_Filter_System] 2. The Dual-Filter System: Isolating the Sweet Spot

This strategy uses a two-dimensional filtering system to identify the ideal conditions for a mean reversion trade.

- **[FILTER: Participation_Filter] Relative Volume (RVOL):** The RVOL, normalized for time-of-day, is used to screen out trending environments. A low RVOL reading confirms the absence of strong directional pressure.
    - **Rule:** `RVOL < 0.8`. This threshold, derived from backtesting, provides the best risk-adjusted return by filtering out adverse trending conditions while retaining a sufficient number of trades.
- **[FILTER: Directionality_Filter] Choppiness Index (CI):** This indicator measures the "trendiness" of price action. It is used to screen out unprofitable, random chop.
    - **Rule:** `Choppiness Index (14-period) < 62`. This filters for markets that are quiet but still have enough directional coherence to revert to the mean, avoiding purely random noise.

### [CONCEPT: Implementation_and_Execution] 3. Strategy Implementation and Execution

- **[UNIVERSE]** Highly liquid, large-capitalization equities where HFT market-making and VWAP anchoring are most pronounced.
- **[ENTRY_TRIGGER]** The entry signal is generated when the price touches or briefly penetrates the **±2.0 VWAP Standard Deviation Band**. This represents a statistically significant, two-sigma deviation from the volume-weighted mean, signaling a high-probability reversion setup.
- **[EXIT_LOGIC]**
    - **Primary Profit Target:** The central VWAP line. This is the logical and highest-probability target.
    - **Primary Stop-Loss:** A volatility-based stop using a multiple of the Average True Range (e.g., 1.5x ATR) provides a dynamic risk buffer.
    - **Time Stop:** A hard, non-negotiable time-of-day exit (e.g., 2:45 PM ET) is mandatory to ensure the position is not held into the high-momentum closing period, where the strategy's core premise is no longer valid.

### [CONCEPT: Performance_Profile] 4. Performance Profile

- **Expectancy:** This is a high-frequency, small-edge strategy. It is characterized by a high win rate (often >60%) but a low average payoff (risk/reward ratio). Profitability is derived from a large number of small, consistent wins, not from large outlier gains.
- **Key Risk:** The strategy is highly sensitive to transaction costs. It is only viable on instruments with very tight bid-ask spreads.