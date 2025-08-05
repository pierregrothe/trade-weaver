# [CONCEPT: Market_Regime] Market Regime Analysis Module

This document provides the definitive guide for the AI's "situational awareness" module. Its sole purpose is to quantitatively analyze the broader market context and produce a machine-readable `market_regime` state object. This state object is the primary input for the agent's master strategy selection logic.

### [PRINCIPLE: Situational_Awareness] The Importance of Situational Awareness

A strategy's success is critically dependent on the environment in which it is deployed. A perfect agent does not blindly execute signals; it first assesses the overall market "weather" and then chooses the appropriate strategy. This module provides that assessment.

### [COMPONENT: Volatility] 1. Volatility Analysis (The "Fear Gauge")

- **[INDICATOR]** CBOE Volatility Index (VIX).
- **[LOGIC]** The agent must query the real-time VIX value.
- **[THRESHOLDS]** The value is classified into one of three states:
  - `VIX < 20`: **[STATE: Low_Volatility]**. Characterized by investor complacency, stable trends, or calm ranges. Favorable for Momentum and Mean Reversion. Unfavorable for Breakouts.
  - `20 <= VIX <= 30`: **[STATE: Medium_Volatility]**. Heightened risk awareness. Optimal for Breakouts; still good for Momentum and Mean Reversion.
  - `VIX > 30`: **[STATE: High_Volatility]**. Significant market fear. Optimal for powerful Breakouts, but **unfavorable and dangerous for Momentum** (due to crash risk) and risky for Mean Reversion (due to trend persistence risk).

### [COMPONENT: Trend] 2. Trend Analysis (The "Directional Conviction")

- **[INDICATOR]** Average Directional Index (ADX) with a 14-period setting, applied to a broad market proxy (e.g., QQQ ETF for NASDAQ 100).
- **[LOGIC]** The agent must query the current ADX value.
- **[THRESHOLDS]** The value is classified into one of two states:
  - `ADX < 25`: **[STATE: Ranging_Market]**. Weak or non-existent trend. Favorable for Mean Reversion. Unfavorable for Momentum.
  - `ADX > 25`: **[STATE: Trending_Market]**. A strengthening trend exists. Favorable for Momentum and Breakout follow-through. **Unfavorable and dangerous for Mean Reversion**.

### [COMPONENT: Time] 3. Time-of-Day Analysis (The "Activity Cycle")

- **[PRINCIPLE]** Intraday volume and volatility follow a predictable U-shaped pattern.
- **[LOGIC]** The agent must classify the current time into one of three states:
  - `09:30 - 10:30 ET`: **[STATE: Opening_Hour]**. High volume and volatility, ideal for trend-setting and breakouts.
  - `10:30 - 15:00 ET`: **[STATE: Midday_Lull]**. Low volume and activity, ideal for ranging and mean reversion.
  - `15:00 - 16:00 ET`: **[STATE: Closing_Hour]**. Second wave of high volume, ideal for trend continuation.

### [OUTPUT: State_Object] The `market_regime` State Object

The output of this module is a structured object written to `session.state`, which is read by all other strategy modules.

**Example `market_regime` object:**

```json
{
  "timestamp": "2025-08-05T09:40:00Z",
  "vix_value": 22.5,
  "vix_state": "Medium_Volatility",
  "adx_value": 28.1,
  "adx_state": "Trending_Market",
  "time_state": "Opening_Hour",
  "regime_code": "OPENING_TRENDING_MEDIUM_VOL"
}
```

### [CONCEPT: ADK_Implementation] ADK Implementation Pattern

- **[TOOL: `updateMarketRegimeTool`]** The entire logic of this module should be encapsulated in a single `FunctionTool`.
- **[ORCHESTRATION: Root_Agent]** The root `LlmAgent` should be instructed to call this tool at the beginning of its decision loop for every new 5-minute candle.
- **[STATE_MANAGEMENT: `ToolContext`]** The `updateMarketRegimeTool` uses `tool_context.state['market_regime'] = regime_object` to update the central state, making the new regime instantly available to all other tools and the `LlmAgent` itself for its next decision.
