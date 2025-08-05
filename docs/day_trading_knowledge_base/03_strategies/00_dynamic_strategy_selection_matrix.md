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
        adx_state = current_regime.adx_state
    )
    
    # 4. Activate the Recommended Strategy Module
    IF recommended_strategy == 'Breakout':
        CALL execute_orb_strategy_tool()
    ELSE IF recommended_strategy == 'Momentum':
        CALL execute_momentum_strategy_tool()
    ELSE IF recommended_strategy == 'Mean_Reversion':
        CALL execute_mean_reversion_strategy_tool()
    ELSE: # No Trade
        DO_NOTHING_AND_WAIT_FOR_NEXT_CANDLE()
```

### [CONCEPT: Decision_Matrix] The Dynamic Strategy Decision Matrix

This matrix is the quantitative data source queried by the decision algorithm.

| [STATE: Time_of_Day_ET] | [STATE: Market_Regime] | [STRATEGY: Primary_Strategy] | [PARAMETER: Optimal_Parameters] | [METRIC: Expected_Profit_Factor] | [METRIC: Confidence_Score] |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Opening Hour** (9:30-10:30) | Med-High VIX / Ranging ADX (Prior Day) | **Breakout (ORB)** | 15-min Range, EOC Target, Vol > 2x Avg | **> 1.75** | **5/5** |
| | Low-Med VIX / Trending ADX | **Momentum** | EMA 13/48 Crossover, RSI/MACD Filter | **~1.85** | **4/5** |
| | All Other Regimes | **No Trade** | N/A | < 1.0 | 1/5 |
| **Midday Lull** (10:30-15:00) | Low-Med VIX / Ranging ADX | **Mean Reversion** | BB(10, 1.5) & RSI(9) @ 75/25 | **~1.85** | **5/5** |
| | Low-Med VIX / Trending ADX | **Momentum** | EMA 13/48 Crossover, RSI/MACD Filter | **~1.08** | **2/5** |
| | All Other Regimes | **No Trade** | N/A | < 1.0 | 1/5 |
| **Closing Hour** (15:00-16:00) | Low-Med VIX / Trending ADX | **Momentum** | EMA 13/48 Crossover, RSI/MACD Filter | **~1.79** | **5/5** |
| | Low-Med VIX / Ranging ADX | **Mean Reversion** | BB(10, 1.5) & RSI(9) @ 75/25 | **~1.28** | **3/5** |
| | All Other Regimes | **No Trade** | N/A | < 1.0 | 1/5 |

[SOURCE_ID: Quantitative Day Trading Strategy Optimization, Section 1 & 5]
[SOURCE_ID: Intraday Momentum Strategy Analysis, Section 4]
[SOURCE_ID: ORB Strategy Quantitative Analysis, Section 4]
[SOURCE_ID: Intraday Mean Reversion Strategy Analysis, Section 4]
