# [CONCEPT: Trade_Execution_Logic] Trade Execution Logic

This document defines the programmable logic for trade entry, exit, and management. An entry signal is a calculated response to a pattern with a historical statistical edge. All trades are executed programmatically with **[TECHNIQUE: Bracket_Orders]** to enforce discipline.

### [LOGIC: Pre_Entry_Checks] Pre-Entry Prerequisite Checks

Before evaluating any specific entry strategy for a stock on the watchlist, the following prerequisite checks must pass. This ensures the broader market context is aligned with the intended trade.

1. **[CHECK: Market_Regime] Market Regime Filter:**
    - `IF system_state == 'Mid-Day' AND strategy_type == 'Momentum' THEN REJECT_ALL_SIGNALS`. Momentum strategies are only permitted during the 'Open' state.
    - `IF system_state == 'Open' AND strategy_type == 'Mean_Reversion' THEN REJECT_ALL_SIGNALS`. Mean reversion strategies are only permitted during the 'Mid-Day' state.
2. **[CHECK: Broad_Market_Filter] Broad Market Correlation Filter (for Longs):**
    - To filter out trades that are fighting the overall market trend, check the S&P 500 (SPY) intraday trend.
    - `IF proposed_trade_direction == 'LONG' AND spy_price < spy_vwap THEN REJECT_SIGNAL`. Do not take new long positions if the broad market is in a bearish intraday trend.

### [LOGIC: Entry_Strategies] Entry Strategy Logic

If prerequisites are met, the agent evaluates signals from its active strategy modules.

- **[STRATEGY: Breakout]**
  - **[ENTRY_RULE: Long]** `IF price.crosses_above(pre_market_high) AND volume > (volume_ma(20) * 2.0) THEN EXECUTE_LONG_BRACKET_ORDER`.
  - **[EXIT_RULE: Stop_Loss]** Place initial stop-loss at `pre_market_high - (0.5 * atr(14))`. The stop is placed *below* the breakout level.
- **[STRATEGY: Dip_Buy]** (Trend-Following)
  - **[ENTRY_RULE: Long]** `IF price > vwap AND price.pulls_back_to_touch(ema(9)) AND prints_bullish_reversal_candle() THEN EXECUTE_LONG_BRACKET_ORDER`.
  - **[EXIT_RULE: Stop_Loss]** Place initial stop-loss just below the low of the bullish reversal candle.
- **[STRATEGY: Mean_Reversion]** (Counter-Trend)
  - **[ENTRY_RULE: Long]** `IF rsi(14) < 30 AND price.touches(lower_bollinger_band) THEN EXECUTE_LONG_BRACKET_ORDER`.
  - **[EXIT_RULE: Profit_Target]** This strategy has a **non-negotiable** profit target: `sma(20)` (the middle Bollinger Band).
  - **[EXIT_RULE: Stop_Loss]** Place initial stop-loss just below the low of the entry candle.

### [LOGIC: Trade_Management] In-Trade Management Logic

Once a position is open, the management module takes over.

- **[TECHNIQUE: Scaling_Out] Scaling Out for Profit Protection:**
  - **[RULE: First_Target]** `IF position.pnl_per_share >= (initial_risk_per_share * 2.0) THEN SELL 50% of position`.
  - **[RULE: Move_Stop_to_Breakeven]** `AFTER_FIRST_TARGET_SELL, MOVE stop_loss_price = entry_price`. This makes the remainder of the trade risk-free.
- **[TECHNIQUE: Trailing_Stops] Dynamic Trailing Stops for Remainder:**
  - **[RULE: Trailing_Stop_Logic]** For the remaining 50% of the position, the stop-loss is continuously updated.
  - `SET stop_loss_price = current_high_since_entry - (2.0 * atr(14))`. This trails the stop below the recent highs, adapting to volatility while locking in gains.

[SOURCE_ID: The Definitive Day Trading Manual for the Québec-Based Trader, Part 1]
[SOURCE_ID: Day Trading AI Agent Build, Section 3.1]
[SOURCE_ID: AI Day Trading Blueprint, Section 3]
