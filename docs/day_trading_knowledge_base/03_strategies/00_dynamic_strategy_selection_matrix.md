# [CONCEPT: Strategy_Selection_Matrix] The Agent's Core Decision Loop

This document provides the master decision-making algorithm for the AI agent. It allows the agent to dynamically select the optimal trading strategy based on the `market_regime` state object, which is continuously updated by the Market Regime Analysis Module.

### [PRINCIPLE: Decision_Algorithm] The Decision Algorithm (Pseudocode)

The agent's master controller must execute the following logic at the start of each 5-minute candle:

```python
# [PSEUDOCODE: Master_Decision_Loop]
FUNCTION on_new_candle():
    # 1. Update Situational Awareness
    CALL updateMarketRegimeTool()
    
    # 2. Retrieve Current Regime from State
    current_regime = session.state['market_regime']
    
    # 3. Consult the Decision Matrix to get the highest-probability strategy
    recommended_strategy = query_decision_matrix(
        time_state = current_regime.time_state,
        vix_state = current_regime.vix_state,
        adx_state = current_regime.adx_state,
        has_catalyst = check_for_news_catalyst(session.state['watchlist'])
    )
    
    # 4. Activate the Recommended Strategy Module
    IF recommended_strategy == 'Breakout':
        CALL execute_orb_strategy_tool()
    ELSE IF recommended_strategy == 'Momentum':
        CALL execute_momentum_strategy_tool()
    ELSE IF recommended_strategy == 'Mean_Reversion':
        CALL execute_mean_reversion_strategy_tool()
    ELSE IF recommended_strategy == 'News_Based':
        CALL execute_news_based_strategy_tool()
    ELSE: # No Trade
        DO_NOTHING_AND_WAIT_FOR_NEXT_CANDLE()
```

### [CONCEPT: Decision_Matrix] The Exhaustive Dynamic Strategy Decision Matrix

This matrix is the quantitative data source queried by the decision algorithm. It maps market conditions to the highest-probability strategy.

| [STATE: Time_of_Day_ET] | [STATE: Volatility (VIX)] | [STATE: Trend (ADX)] | [STATE: Catalyst] | [STRATEGY: Primary] | [STRATEGY: Secondary] | [METRIC: Confidence] |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Opening Hour** (9:30-10:30) | Low (<20) | Trending (>25) | Yes | **News-Based (Gap & Go)** | Momentum | 5/5 |
| | Low (<20) | Trending (>25) | No | **Momentum** | Breakout (ORB) | 4/5 |
| | Low (<20) | Ranging (<25) | Yes | **News-Based (Gap Fade)** | Mean Reversion | 3/5 |
| | Low (<20) | Ranging (<25) | No | **No Trade** | - | 1/5 |
| | Medium (20-30) | Trending (>25) | Yes | **News-Based (Gap & Go)** | Breakout (ORB) | 5/5 |
| | Medium (20-30) | Trending (>25) | No | **Breakout (ORB)** | Momentum | 4/5 |
| | Medium (20-30) | Ranging (<25) | Yes | **News-Based (Gap Fade)** | Mean Reversion | 4/5 |
| | Medium (20-30) | Ranging (<25) | No | **Mean Reversion** | No Trade | 3/5 |
| | High (>30) | Any | Yes | **News-Based (Volatility Play)** | Scalping | 4/5 |
| | High (>30) | Any | No | **Scalping** | No Trade | 3/5 |
| **Midday Lull** (10:30-15:00) | Low (<20) | Ranging (<25) | No | **Mean Reversion** | No Trade | 5/5 |
| | Low (<20) | Trending (>25) | No | **Momentum (Continuation)** | No Trade | 3/5 |
| | Medium (20-30) | Ranging (<25) | No | **Mean Reversion** | Scalping | 4/5 |
| | High (>30) | Any | No | **Scalping** | No Trade | 4/5 |
| **Closing Hour** (15:00-16:00) | Low-Med (<30) | Trending (>25) | No | **Momentum (Trend Close)** | No Trade | 5/5 |
| | Low-Med (<30) | Ranging (<25) | No | **Mean Reversion** | No Trade | 3/5 |

[SOURCE_ID: Quantitative Day Trading Strategy Optimization, Section 1 & 5]
[SOURCE_ID: Intraday Momentum Strategy Analysis, Section 4]
[SOURCE_ID: ORB Strategy Quantitative Analysis, Section 4]
[SOURCE_ID: Intraday Mean Reversion Strategy Analysis, Section 4]
[SOURCE_ID: Expanded Day Trading Knowledge Base: Market Regimes, Indicators, and Strategies_chatGPT.md]
