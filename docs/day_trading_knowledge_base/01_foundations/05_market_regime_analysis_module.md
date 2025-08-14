# [CONCEPT: Market_Regime] Market Regime Analysis Module

This document provides the definitive guide for the AI's "situational awareness" module. Its sole purpose is to quantitatively analyze the broader market context and produce a machine-readable `market_regime` state object. This state object is the primary input for the agent's master strategy selection logic.

### [PRINCIPLE: Situational_Awareness] The Importance of Situational Awareness

A strategy's success is critically dependent on the environment in which it is deployed. A perfect agent does not blindly execute signals; it first assesses the overall market "weather" and then chooses the appropriate strategy. This module provides that assessment by moving from simple heuristics to advanced probabilistic models.

### [COMPONENT: Volatility] 1. Volatility Analysis (The "Fear Gauge")

- **[INDICATOR]** CBOE Volatility Index (VIX) for broad market sentiment and Average True Range (ATR) for instrument-specific volatility.
- **[LOGIC]** The agent must query the real-time VIX value and calculate the 14-day ATR for the specific instrument being considered.
- **[THRESHOLDS]** The VIX value is classified into one of three states:
  - `VIX < 15-20`: **[STATE: Low_Volatility]**. Characterized by investor complacency and stable trends. Favorable for trend-following strategies.
  - `20 <= VIX <= 30`: **[STATE: Medium_Volatility]**. Heightened risk awareness. Optimal for Breakouts.
  - `VIX > 30`: **[STATE: High_Volatility]**. Significant market fear. Price swings are large and rapid, making mean-reversion and scalping more viable. Unfavorable for classic trend-following due to reversal risk.

### [COMPONENT: Trend] 2. Trend Analysis (The "Directional Conviction")

- **[INDICATOR]** Average Directional Index (ADX) with a 14-period setting, applied to a broad market proxy (e.g., QQQ ETF) and the specific instrument.
- **[LOGIC]** The agent must query the current ADX value.
- **[THRESHOLDS]** The value is classified into states:
  - `ADX < 20-25`: **[STATE: Ranging_Market]**. Weak or non-existent trend. Favorable for Mean Reversion. Unfavorable for Momentum.
  - `ADX > 25`: **[STATE: Trending_Market]**. A strengthening trend exists. Favorable for Momentum and Breakout follow-through.
  - `ADX > 40`: **[STATE: Very_Strong_Trend]**. An extremely strong trend that may be nearing exhaustion, warranting caution.

### [COMPONENT: Time] 3. Time-of-Day Analysis (The "Activity Cycle")

- **[PRINCIPLE]** Intraday volume and volatility follow a predictable U-shaped pattern.
- **[LOGIC]** The agent must classify the current time into one of three states:
  - `09:30 - 10:30 ET`: **[STATE: Opening_Hour]**. The most volatile and liquid period. Ideal for trend-setting, breakouts, and Gap-and-Go strategies.
  - `10:30 - 15:00 ET`: **[STATE: Midday_Lull]**. Low volume and activity. Aggressive momentum plays are riskier. Favorable for mean-reversion and scalping small ranges.
  - `15:00 - 16:00 ET`: **[STATE: Closing_Hour]**. Second wave of high volume as positions are closed. Ideal for trend continuation.

### [COMPONENT: Advanced_Modeling] 4. Advanced Probabilistic and Non-Parametric Models

For a deeper, more robust diagnosis, the agent should employ advanced statistical models.

- **[MODEL: Hidden_Markov_Model] Hidden Markov Models (HMM):** An HMM can be trained on historical returns and volatility to identify unobservable "hidden" states (e.g., 'Low-Vol Trend', 'High-Vol Range'). The model's output is a probability vector (e.g., `P(State=A) = 0.7, P(State=B) = 0.3`), providing a confidence score for the regime classification.
- **[MODEL: GARCH] GARCH Models:** GARCH models are used to forecast short-term volatility, capturing the "volatility clustering" effect. This is critical for dynamic position sizing and risk management.
- **[MODEL: Non_Parametric_Tests] Non-Parametric Tests for Structural Breaks:**
    - **Wasserstein Distance & Kolmogorov-Smirnov (KS) Test:** These tests can detect sudden, significant shifts in the distribution of returns, acting as an early warning system for a fundamental regime change. A spike in these metrics triggers a full re-evaluation of the market state.

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
  "hmm_state_probabilities": {
    "Low-Vol_Trend": 0.15,
    "High-Vol_Range": 0.85
  },
  "regime_code": "OPENING_TRENDING_MEDIUM_VOL_HVR"
}
```


