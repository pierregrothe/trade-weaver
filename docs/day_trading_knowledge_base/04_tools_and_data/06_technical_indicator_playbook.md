# [CONCEPT: Indicator_Playbook] Technical Indicator Playbook for AI Agents

This document moves beyond indicator definitions to provide a professional playbook on how to **combine** indicators for high-probability signals. The core principle is **Signal Confluence**: a trade signal is only considered high-probability if it is confirmed by multiple, non-correlated indicators.

### [PRINCIPLE: Signal_Confluence] The Principle of Signal Confluence

An AI agent must not trade on a single indicator signal in isolation. A high-quality signal requires confirmation from indicators measuring different market dimensions (e.g., Trend + Momentum + Volume). This playbook provides specific combinations for the agent's core strategies.

### [PLAYBOOK: Momentum] Playbook 1: Momentum/Trend-Following Entry

- **[WHAT]** This combination is used to confirm a new, strong trend is likely underway.
- **[WHY]** It ensures the agent enters on a confirmed shift in momentum that is backed by institutional participation and has sufficient strength to continue.
- **[HOW] The Indicator Stack:**
    1. **Trend Filter (`ema(20)` vs. `ema(50)`):** Is the broader context bullish or bearish?
    2. **Entry Trigger (`ema(9)` vs. `ema(20)`):** Has short-term momentum accelerated in the direction of the trend?
    3. **Momentum Confirmation (`MACD`):** Is the underlying momentum strengthening?
    4. **Institutional Confirmation (`VWAP`):** Is the price above/below the day's "fair value" benchmark?
- **[PROGRAMMABLE_RULE: Long_Entry]**
    `FUNCTION checkForMomentumLongSignal():`
    `is_uptrend = ema(20) > ema(50)`
    `is_bullish_cross = ema(9).crosses_above(ema(20))`
    `has_momentum = macd.line > macd.signal AND macd.histogram > 0`
    `has_inst_support = price > vwap`
    `RETURN is_uptrend AND is_bullish_cross AND has_momentum AND has_inst_support`

### [PLAYBOOK: Breakout] Playbook 2: Breakout Confirmation

- **[WHAT]** This combination confirms the validity of a price breakout from a consolidation pattern.
- **[WHY]** Its sole purpose is to filter out "false breakouts" which are a primary cause of losses in this strategy.
- **[HOW] The Indicator Stack:**
    1. **Volatility Compression (`Bollinger_Band_Width`):** Did the breakout emerge from a period of low volatility (a "squeeze")?
    2. **Price Action (`close` vs. `resistance_level`):** Did the price close decisively above resistance?
    3. **Volume Confirmation (`volume` vs. `volume_ma(20)`):** Was the breakout accompanied by a massive surge in volume? This is **non-negotiable**.
- **[PROGRAMMABLE_RULE: Breakout_Entry]**
    `FUNCTION checkForBreakoutSignal(resistance_level):`
    `was_squeezing = bollinger_band_width.is_at_multiday_low()`
    `is_price_breakout = price.closes_above(resistance_level)`
    `has_volume_thrust = volume > (volume_ma(20) * 2.0)`
    `RETURN was_squeezing AND is_price_breakout AND has_volume_thrust`

### [PLAYBOOK: Mean_Reversion] Playbook 3: Mean Reversion Entry

- **[WHAT]** This combination identifies a high-probability setup for a counter-trend trade in a ranging market.
- **[WHY]** It confirms that a price move is not just statistically extended, but also that the momentum driving it is exhausted, increasing the probability of a reversion.
- **[HOW] The Indicator Stack:**
    1. **Trend Filter (`ADX`):** Is the market actually in a ranging state? This is a **mandatory prerequisite check**.
    2. **Statistical Deviation (`Bollinger_Bands`):** Has the price reached a statistically significant extreme (e.g., 1.5 standard deviations from the mean)?
    3. **Momentum Exhaustion (`RSI`):** Is momentum at an overbought/oversold level?
- **[PROGRAMMABLE_RULE: Oversold_Long_Entry]**
    `FUNCTION checkForMeanReversionLongSignal():`
    `is_ranging = adx(14) < 25`
    `is_stat_extreme = price.touches(lower_bollinger_band(10, 1.5))`
    `is_momentum_exhausted = rsi(9) < 25`
    `RETURN is_ranging AND is_stat_extreme AND is_momentum_exhausted`

### [CONCEPT: ADK_Implementation] ADK Implementation Note

- **[TOOL: `FunctionTool`]** Each of these playbooks should be implemented as a separate, complex `FunctionTool`. The agent's `LlmAgent` instruction is simplified to: `"If you believe a momentum opportunity exists, call the checkForMomentumSignalTool and act on its boolean response."`

[SOURCE_ID: Day Trading AI Agent Research, Part IV]
