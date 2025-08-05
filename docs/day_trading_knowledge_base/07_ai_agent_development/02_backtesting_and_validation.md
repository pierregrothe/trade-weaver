# [CONCEPT: Backtesting] The Science of Strategy Validation: Backtesting

An idea for a trading strategy is merely a hypothesis. Before risking real capital, this hypothesis must be subjected to a rigorous, scientific process of validation known as backtesting. A poorly designed backtester that produces overly optimistic results is more dangerous than no backtester at all.

### [CONCEPT: Backtesting_Engine_Architecture] Backtesting Engine Architecture for AI Agent

A professional-grade backtesting engine for an AI agent must be event-driven and consist of several key, decoupled modules:

1. **[MODULE: Data_Handler] Data Handler:** Responsible for loading historical market data (bar by bar or tick by tick) from the database (e.g., BigQuery) and feeding it into the system as a series of time-stamped market data events.
2. **[MODULE: Strategy] Strategy Module:** This is a programmatic representation of the AI's trading logic (e.g., the Momentum or Mean Reversion strategy). It receives market data events and generates `Signal` events (e.g., `GO_LONG`, `GO_SHORT`).
3. **[MODULE: Portfolio_Risk_Manager] Portfolio & Risk Manager:** This module receives `Signal` events. It performs the critical risk management and position sizing calculations (1% rule, portfolio heat, etc.). If the signal passes the risk filters, it generates an `Order` event.
4. **[MODULE: Execution_Simulator] Execution Simulator:** This module receives `Order` events. It simulates the execution of the trade, realistically modeling latency, slippage, and commissions. It then generates a `Fill` event, confirming the trade has been "executed." The Portfolio Manager then updates its state based on the `Fill` event.

### [CONCEPT: Event_Driven_Loop] Event-Driven Backtesting Loop (Pseudocode)

The entire backtest runs inside a time-ordered event loop. This is the core logic:

```python
# [PSEUDOCODE: Backtest_Loop]
event_queue = initialize_event_queue()
data_handler = DataHandler(source_data, event_queue)
strategy = StrategyModule(event_queue)
portfolio_manager = PortfolioManager(event_queue)
execution_simulator = ExecutionSimulator(event_queue)

# Main Event Loop
WHILE True:
    IF data_handler.is_finished() and event_queue.is_empty():
        BREAK

    event = event_queue.get_next_event() # Events are time-ordered

    IF event.type == 'MARKET_DATA':
        portfolio_manager.update_holdings(event) # Update P&L of open positions
        strategy.evaluate_signals(event) # Strategy looks for new trades

    ELSE IF event.type == 'SIGNAL':
        portfolio_manager.generate_order(event) # Risk-check the signal

    ELSE IF event.type == 'ORDER':
        execution_simulator.execute_order(event) # Simulate the trade

    ELSE IF event.type == 'FILL':
        portfolio_manager.update_on_fill(event) # Update portfolio with the new trade

# After loop, generate performance report from portfolio_manager
generate_performance_report(portfolio_manager)
```

### [RISK: Backtesting_Pitfalls] Catastrophic Pitfalls and Biases

- **[BIAS: Overfitting] Overfitting / Curve-Fitting:** The most significant danger. Capturing historical noise rather than a genuine market edge.
- **[BIAS: Survivorship_Bias] Survivorship Bias:** A fatal error caused by using a dataset that excludes delisted companies. The backtesting engine **must be powered by a point-in-time database** that includes all delisted securities.
- **[BIAS: Look_Ahead_Bias] Look-ahead Bias:** An insidious error where the simulation code accidentally uses future information.

### [CONCEPT: Robust_Validation] Techniques for Robust Validation

- **[TECHNIQUE: Out_of_Sample_Testing] Out-of-Sample (OOS) Testing:** Partition data. Develop on in-sample data, validate once on out-of-sample data. A significant performance degradation indicates overfitting.
- **[TECHNIQUE: Walk_Forward_Analysis] Walk-Forward Analysis (WFA):** The gold standard. A rolling OOS test that simulates real-world adaptation to changing market regimes.
- **[TECHNIQUE: Forward_Testing] Forward Testing (Paper Trading):** The final step before deployment. The fully developed strategy is run in a live simulated environment (paper trading) to test its performance in current market conditions and validate the full tech stack.

[SOURCE_ID: Day Trading AI Agent Research, Section 5.2]
[SOURCE_ID: The Definitive Day Trading Manual for the Québec-Based Trader, Part 4]
