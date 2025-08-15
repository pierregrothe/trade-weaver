# [CONCEPT: Strategy_Selection_Matrix] The Agent's Core Decision Loop: A Dynamic Strategy Selection Matrix

This document provides the master decision-making algorithm for the AI agent. It allows the agent to dynamically select the optimal trading strategy based on the `market_regime` state object, which is continuously updated by the Market Regime Analysis Module. The goal is to move beyond a static, one-size-fits-all approach to a dynamic one that adapts to the market's ever-changing character.

### [PRINCIPLE: Decision_Algorithm] The Decision Algorithm (Pseudocode)

The agent's master controller must execute the following logic at the start of each 5-minute candle:

```python
# [PSEUDOCODE: Master_Decision_Loop]
FUNCTION on_new_candle(instrument):
    # 1. Update Situational Awareness
    market_regime = get_market_regime_state()
    instrument_context = get_instrument_context(instrument)

    # 2. Consult the Decision Matrix to get the highest-probability strategy
    # The matrix returns a primary strategy and a confidence score
    strategy_profile = query_decision_matrix(
        time_state = market_regime.time_state,
        vix_state = market_regime.vix_state,
        adx_state = market_regime.adx_state,
        has_catalyst = instrument_context.has_strong_catalyst
    )

    # 3. Activate the Recommended Strategy Module if confidence is sufficient
    IF strategy_profile.confidence > 3:
        activate_strategy_module(strategy_profile.primary_strategy, instrument)
    ELSE:
        # No high-confidence setup, remain idle
        log("No trade signal. Confidence too low.")
```

### [CONCEPT: Decision_Matrix] The Exhaustive Dynamic Strategy Decision Matrix

This matrix is the quantitative data source queried by the decision algorithm. It maps market conditions to the highest-probability strategy. The confidence score is critical for preventing the agent from trading in low-probability environments.

| Time of Day (ET) | Volatility (VIX) | Trend (ADX) | Catalyst Present? | Primary Strategy | Secondary Strategy | Confidence (1-5) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Opening Hour** (9:30-10:30) | Low (<20) | Trending (>25) | Yes | **News-Based (Gap & Go)** | Momentum | 5 |
| | Low (<20) | Trending (>25) | No | **Momentum** | Breakout (ORB) | 4 |
| | Low (<20) | Ranging (<25) | Yes | **News-Based (Gap Fade)** | Mean Reversion | 3 |
| | Low (<20) | Ranging (<25) | No | **No Trade** | - | 1 |
| | Medium (20-30) | Trending (>25) | Yes | **News-Based (Gap & Go)** | Breakout (ORB) | 5 |
| | Medium (20-30) | Trending (>25) | No | **Breakout (ORB)** | Momentum | 4 |
| | Medium (20-30) | Ranging (<25) | Yes | **News-Based (Gap Fade)** | Mean Reversion | 4 |
| | Medium (20-30) | Ranging (<25) | No | **Mean Reversion** | No Trade | 3 |
| | High (>30) | Any | Yes | **News-Based (Volatility Play)** | Scalping | 4 |
| | High (>30) | Any | No | **Scalping** | No Trade | 3 |
| **Midday Lull** (10:30-15:00) | Low (<20) | Ranging (<25) | No | **Mean Reversion** | No Trade | 5 |
| | Low (<20) | Trending (>25) | No | **Momentum (Continuation)** | No Trade | 3 |
| | Medium (20-30) | Ranging (<25) | No | **Mean Reversion** | Scalping | 4 |
| | High (>30) | Any | No | **Scalping** | No Trade | 4 |
| **Closing Hour** (15:00-16:00) | Low-Med (<30) | Trending (>25) | No | **Momentum (Trend Close)** | No Trade | 5 |
| | Low-Med (<30) | Ranging (<25) | No | **Mean Reversion** | No Trade | 3 |

[SOURCE_ID: Quantitative Day Trading Strategy Optimization, Section 1 & 5]
[SOURCE_ID: Intraday Momentum Strategy Analysis, Section 4]
[SOURCE_ID: ORB Strategy Quantitative Analysis, Section 4]
[SOURCE_ID: Intraday Mean Reversion Strategy Analysis, Section 4]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]