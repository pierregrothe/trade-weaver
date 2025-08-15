# [CONCEPT: Market_Regime] Market Regime Analysis Module

This document provides the definitive guide for the AI's "situational awareness" module. Its sole purpose is to quantitatively analyze the broader market context and produce a machine-readable `market_regime` state object. This state object is the primary input for the agent's master strategy selection logic.

### [PRINCIPLE: Situational_Awareness] The Importance of Situational Awareness

A strategy's success is critically dependent on the environment in which it is deployed. A perfect agent does not blindly execute signals; it first assesses the overall market "weather" and then chooses the appropriate strategy. This module provides that assessment by moving from simple heuristics to advanced probabilistic models.

### [COMPONENT: Volatility] 1. Volatility Analysis (The "Fear Gauge")

- **[INDICATOR]** CBOE Volatility Index (VIX) for broad market sentiment and Average True Range (ATR) for instrument-specific volatility.
- **[LOGIC]** The agent must query the real-time VIX value and its term structure.
- **[THRESHOLDS]** The VIX value is classified into states:
  - `VIX < 18`: **[STATE: Low_Volatility]**. Complacent market, favorable for trend-following strategies.
  - `VIX 18-25`: **[STATE: Medium_Volatility]**. Normal risk awareness. Favorable for most strategies.
  - `VIX 25-35`: **[STATE: High_Volatility]**. Significant market fear. Price swings are large and rapid. Risk parameters should be tightened.
  - `VIX > 35`: **[STATE: Extreme_Volatility]**. Market panic. Cease all new trade initiation and focus on managing existing positions.
- **[ADVANCED_SIGNAL: VIX_Term_Structure]** The relationship between short-term and long-term VIX futures is more predictive than the spot price. 
    - **Contango (Normal):** Short-term futures < Long-term futures. Indicates normal market conditions.
    - **Backwardation (Fear):** Short-term futures > Long-term futures. A powerful signal of immediate market stress. The agent should adopt a more defensive posture when the curve is in backwardation, regardless of the spot VIX level.

### [COMPONENT: Trend] 2. Trend Analysis (The "Directional Conviction")

- **[INDICATOR]** Average Directional Index (ADX) with a 14-period setting, applied to a broad market proxy (e.g., QQQ ETF).
- **[LOGIC]** The agent must query the ADX value and the state of its component lines, the Positive Directional Indicator (+DI) and Negative Directional Indicator (-DI).
- **[THRESHOLDS]**
  - `ADX < 25`: **[STATE: Ranging_Market]**. Weak or non-existent trend. Favorable for Mean Reversion.
  - `ADX > 25`: **[STATE: Trending_Market]**. A strengthening trend exists. The direction is confirmed by the dominant DI line (e.g., `+DI > -DI` for an uptrend).
  - `ADX_Slope < 0 AND ADX > 40`: **[STATE: Trend_Exhaustion]**. A high but falling ADX can signal a trend that is losing momentum and may be prone to reversal.

### [COMPONENT: Time] 3. Time-of-Day Analysis (The "Activity Cycle")

- **[PRINCIPLE]** Intraday volume and volatility follow a predictable U-shaped pattern.
- **[LOGIC]** The agent must classify the current time into one of three states:
  - `09:30 - 10:30 ET`: **[STATE: Opening_Hour]**. Most volatile and liquid. Ideal for breakouts.
  - `10:30 - 15:00 ET`: **[STATE: Midday_Lull]**. Low volume and activity. Favorable for mean-reversion.
  - `15:00 - 16:00 ET`: **[STATE: Closing_Hour]**. Second wave of high volume. Ideal for trend continuation.

### [COMPONENT: Advanced_Modeling] 4. Advanced Probabilistic and Non-Parametric Models

- **[MODEL: Hidden_Markov_Model] Hidden Markov Models (HMM):** An HMM infers the market's hidden "personality" (e.g., 'Calm Bull', 'Volatile Bear') from observable data like returns. The model's output is a probability vector (e.g., `P(State=A) = 0.7, P(State=B) = 0.3`), providing a confidence score for the regime classification that can be used for dynamic strategy weighting.
- **[MODEL: GARCH] GARCH Models:** While VIX gives a broad market view, a GARCH model provides a specific, quantitative forecast for the *next day's expected volatility for a single asset*, allowing for more precise, instrument-specific risk management.
- **[MODEL: Non_Parametric_Tests] Kolmogorov-Smirnov (KS) Test for Structural Breaks:** The KS-test acts as a high-sensitivity regime change detector. The agent continuously compares the "fingerprint" (return distribution) of recent data (e.g., last 30 days) to a longer-term baseline. A statistically significant divergence (e.g., p-value < 0.05) signals a structural break, prompting a re-evaluation of all strategy parameters.

### [OUTPUT: State_Object] The `market_regime` State Object

The output of this module is a structured object written to `session.state`, which is read by all other strategy modules.

**Example `market_regime` object:**

```json
{
  "timestamp": "2025-08-05T14:30:00Z",
  "vix_value": 17.5,
  "vix_state": "Low_Volatility",
  "vix_term_structure": "Contango",
  "adx_value": 19.8,
  "adx_slope": -0.5,
  "adx_state": "Ranging_Market",
  "time_state": "Midday_Lull",
  "hmm_state_probabilities": {
    "Low-Vol_Range": 0.85,
    "High-Vol_Trend": 0.15
  },
  "ks_test_p_value": 0.45,
  "regime_code": "MIDDAY_RANGING_LOW_VOL_LVR"
}
```