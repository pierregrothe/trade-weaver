# [CONCEPT: Technical_Indicators] Technical Indicators Decoded

This document is a reference library for the mathematical tools used to analyze market data. For an AI, these transform raw data into structured, actionable features.

### [CONCEPT: Indicator_Hierarchy] Hierarchy and Role of Indicators

A robust trading signal comes from **confirmation**, not from a single indicator. The agent's strategies must be built on a combination of indicators from different categories. Using multiple indicators from the same category (e.g., RSI, Stochastics, and MACD together) is a common error that leads to multicollinearity and false confidence.

- **1. Trend Indicators (The "Context"):** Define the overall market direction. Is the market trending or ranging? `(e.g., Moving Averages)`
- **2. Momentum Indicators (The "Signal"):** Measure the speed and strength of price changes. They provide entry signals *within the context of the trend*. `(e.g., MACD, RSI)`
- **3. Volatility Indicators (The "Risk"):** Measure the magnitude of price swings. They are critical for setting stop-loss levels and profit targets. `(e.g., Bollinger Bands, ATR)`
- **4. Volume Indicators (The "Confirmation"):** Measure the conviction behind a price move. A price move on high volume is more significant than one on low volume. `(e.g., VWAP, Volume MA)`

### [INDICATOR: Moving_Average] Moving Averages (MA, SMA, EMA) - Trend

- **[CALCULATION:]** Averages price over a set number of periods. EMA gives more weight to recent prices and is preferred for day trading.
- **[INTERPRETATION:]** A rising EMA indicates an uptrend; a falling EMA signals a downtrend. They act as dynamic support and resistance.
- **[STRATEGY: Crossover]** A short-term EMA (e.g., 9-period) crossing above a long-term EMA (e.g., 20-period) is a bullish signal.
- **[AI_BEST_PRACTICE:]** Use a multi-EMA setup (e.g., 9, 20, 50) to define the market trend state (e.g., `IF price > ema(9) > ema(20) > ema(50) THEN market_state = 'Strong_Uptrend'`).

### [INDICATOR: MACD] Moving Average Convergence Divergence - Momentum

- **[CALCULATION:]** Shows the relationship between a 12-period EMA and a 26-period EMA. Consists of the `MACD Line`, a `Signal Line` (9-period EMA of the MACD), and a `Histogram`.
- **[STRATEGY: Crossover]** A bullish signal occurs when the `MACD Line` crosses above the `Signal Line`.
- **[STRATEGY: Divergence]** A powerful reversal signal. Bullish divergence: price makes a lower low, but MACD makes a higher low.
- **[AI_BEST_PRACTICE:]** Use the histogram value as a quantitative measure of momentum strength. A rising histogram confirms accelerating momentum.

### [INDICATOR: RSI] Relative Strength Index - Momentum

- **[CALCULATION:]** Measures the speed and magnitude of price changes, oscillating between 0 and 100.
- **[STRATEGY: Mean_Reversion]** In ranging markets, RSI `> 70` is overbought; `< 30` is oversold.
- **[STRATEGY: Momentum]** In a strong trend, the 50 level acts as support (uptrend) or resistance (downtrend).
- **[AI_BEST_PRACTICE:]** The agent must first classify the market regime. `IF market_state == 'Ranging' THEN use_rsi_for_mean_reversion() ELSE use_rsi_for_momentum_confirmation()`.

### [INDICATOR: Bollinger_Bands] Bollinger Bands - Volatility

- **[CALCULATION:]** A middle band (20-period SMA) and outer bands plotted at two standard deviations. Bands widen with high volatility and narrow ("squeeze") with low volatility.
- **[STRATEGY: Breakout]** A "squeeze" often precedes an explosive breakout. The AI should increase its monitoring of a stock when its Bollinger Band Width reaches a multi-day low.
- **[STRATEGY: Mean_Reversion]** A "Bollinger Bounce" involves selling at the upper band and buying at the lower band in a ranging market.
- **[AI_BEST_PRACTICE:]** Use the distance between the bands as a direct numerical input for the AI's risk module to dynamically adjust stop-loss width.

### [INDICATOR: VWAP] Volume-Weighted Average Price - Volume/Trend

- **[CALCULATION:]** The average price weighted by volume, calculated fresh each day.
- **[INTERPRETATION:]** The institutional benchmark for "fair value" intraday. Price > VWAP is bullish; Price < VWAP is bearish.
- **[STRATEGY: Support_Resistance]** VWAP acts as a significant dynamic support/resistance level. A break across the VWAP on high volume is a powerful signal of a shift in intraday control.
- **[AI_BEST_PRACTICE:]** This is a primary indicator. A `price_vs_vwap` state should be maintained for every stock on the watchlist and used as a prerequisite filter for many entry strategies. For example, `IF proposed_trade == 'LONG' AND price < vwap THEN REJECT_SIGNAL`.

[SOURCE_ID: Day Trading AI Agent Research, Part IV]
