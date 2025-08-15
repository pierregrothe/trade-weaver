# [CONCEPT: Trade_Execution_Logic] Trade Execution Logic

This document defines the programmable logic for trade entry, exit, and management. An entry signal is a calculated response to a pattern with a historical statistical edge. All trades are executed programmatically with **[TECHNIQUE: Bracket_Orders]** to enforce discipline.

### [LOGIC: Pre_Entry_Checks] Pre-Entry Prerequisite Checks

Before evaluating any specific entry strategy, a tiered set of prerequisite checks must pass. This ensures the broader market context and instrument-specific conditions are aligned with the intended trade.

1.  **[CHECK: System_State] System State Filter:** The master state machine must be in an active trading state (`Open` or `Mid-Day`).
2.  **[CHECK: Market_Regime] Market Regime Filter:** The proposed strategy must be valid for the current market regime.
    -   `IF market_regime.vix_state == 'High_Volatility' AND proposed_strategy.type == 'Momentum' THEN REJECT_ALL_SIGNALS`.
    -   `IF market_regime.adx_state == 'Ranging_Market' AND proposed_strategy.type == 'Breakout' THEN REJECT_ALL_SIGNALS`.
3.  **[CHECK: Broad_Market_Filter] Broad Market Correlation Filter (for Longs):** To avoid fighting the overall market trend, check the S&P 500 (SPY) intraday trend.
    -   `IF proposed_trade.direction == 'LONG' AND spy.price < spy.vwap THEN REJECT_SIGNAL`.

### [LOGIC: Entry_Strategies] Entry Strategy Logic

If prerequisites are met, the agent evaluates signals from its active strategy modules.

-   **[STRATEGY: Breakout] Opening Range Breakout**
    -   **[ENTRY_RULE: Long]** `IF price.crosses_above(pre_market_high) AND volume > (volume_ma(20) * 2.0) AND rsi(14) > 55 THEN EXECUTE_LONG_BRACKET_ORDER`.
    -   **[EXIT_RULE: Stop_Loss]** Place initial stop-loss at `pre_market_high - (0.5 * atr(14))`. The stop is placed *below* the breakout level to allow for a minor retest.
    -   **[EXIT_RULE: Profit_Target]** A common initial target is a 2:1 risk/reward ratio. `Profit_Target = entry_price + (2 * (entry_price - stop_loss_price))`.

-   **[STRATEGY: Dip_Buy] VWAP Pullback (Trend-Following)**
    -   **[ENTRY_RULE: Long]** `IF price > vwap AND price.pulls_back_to_touch(ema(9)) AND prints_bullish_reversal_candle() THEN EXECUTE_LONG_BRACKET_ORDER`.
    -   **[EXIT_RULE: Stop_Loss]** Place initial stop-loss just below the low of the bullish reversal candle, defining a tight, clear invalidation point.

-   **[STRATEGY: Mean_Reversion] Bollinger Band Fade (Counter-Trend)**
    -   **[ENTRY_RULE: Long]** `IF rsi(14) < 30 AND price.touches(lower_bollinger_band(20, 2.0)) THEN EXECUTE_LONG_BRACKET_ORDER`.
    -   **[EXIT_RULE: Profit_Target]** This strategy has a **non-negotiable** primary profit target: `sma(20)` (the middle Bollinger Band), representing a return to the mean.
    -   **[EXIT_RULE: Stop_Loss]** Place initial stop-loss just below the low of the entry candle.

### [LOGIC: Trade_Management] In-Trade Management Logic

Once a position is open, the management module takes over. The goal is to protect profits while allowing winning trades room to run.

-   **[TECHNIQUE: Scaling_Out] Scaling Out for Profit Protection:** This is a core technique for improving the strategy's overall profit factor and reducing volatility.
    -   **[RULE: First_Target]** `IF position.pnl_per_share >= (initial_risk_per_share * 2.0) THEN SELL 50% of position`.
    -   **[RULE: Move_Stop_to_Breakeven]** `AFTER_FIRST_TARGET_SELL, MOVE stop_loss_price = entry_price`. This makes the remainder of the trade a "risk-free" runner.
-   **[TECHNIQUE: Trailing_Stops] Dynamic Trailing Stops for Remainder:** For the remaining portion of the position, the stop-loss is continuously updated to lock in gains.
    -   **[RULE: ATR_Trailing_Stop]** A common and effective method is an ATR-based trail.
        `SET stop_loss_price = current_high_since_entry - (2.0 * atr(14))`. This trails the stop below the recent highs, adapting to volatility.

[SOURCE_ID: The Definitive Day Trading Manual for the Québec-Based Trader, Part 1]
[SOURCE_ID: Day Trading AI Agent Build, Section 3.1]
[SOURCE_ID: AI Day Trading Blueprint, Section 3]