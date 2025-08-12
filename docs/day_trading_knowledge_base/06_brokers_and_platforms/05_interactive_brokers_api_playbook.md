# [TOOL: IBKR_API] Interactive Brokers API Playbook

This document provides a practical guide for using the Interactive Brokers (IBKR) API to handle all aspects of trade execution, order management, and portfolio monitoring for the AI agent. We will use the `ib_insync` Python library for its modern, asynchronous approach.

### [PRINCIPLE: Role_in_Architecture] IBKR's Role in the System Architecture

IBKR is our designated execution venue. Its API will be used exclusively for:

1.  **Order Execution:** Placing, modifying, and canceling all trade orders.
2.  **Portfolio Management:** Real-time monitoring of positions, P&L, and account values.
3.  **High-Fidelity Market Data:** While EODHD is our primary data source, IBKR can serve as a secondary, high-fidelity source for real-time data, especially for validating prices just before execution.

### [IMPLEMENTATION: ib_insync] Using the `ib_insync` Library

`ib_insync` provides a clean, Pythonic interface to the native IBKR API. It simplifies the asynchronous communication required for a high-performance trading system.

```python
# Basic setup and connection
from ib_insync import *

# Utility to run async code in a sync environment like a script
util.startLoop()

ib = IB()
# Connect to Trader Workstation (TWS) or IB Gateway
# Ensure TWS/Gateway is running and API connections are enabled
ib.connect('127.0.0.1', 7497, clientId=1)
```

### [USE_CASE: Order_Execution] 1. Advanced Order Execution

The agent's primary interaction with IBKR will be to place sophisticated, risk-managed orders.

-   **[HOW]** The `ib.placeOrder()` method is used to submit orders. The key is to construct the correct `Contract` and `Order` objects.
-   **[ADK_IMPLEMENTATION]** The `execute_trade` `FunctionTool` will be a wrapper around this functionality. It will take the trade signal from the agent, construct the appropriate `BracketOrder`, and place it via the IBKR API.

```python
# Example: Placing a Bracket Order for a long position
contract = Stock('AAPL', 'SMART', 'USD')

# Define the parent entry order and the attached take profit and stop loss orders
bracket_order = ib.bracketOrder(
    action='BUY', 
    quantity=100, 
    limitPrice=150.00, # The entry price
    takeProfitPrice=155.00, # The profit target
    stopLossPrice=148.00 # The stop-loss
)

# Place the entire bracket order
for o in bracket_order:
    ib.placeOrder(contract, o)
```

### [USE_CASE: Portfolio_Monitoring] 2. Real-Time Portfolio and P&L Monitoring

The agent needs a real-time view of its own portfolio to make informed decisions and for the risk management module to function correctly.

-   **[HOW]** The `ib.portfolio()` method returns a list of current positions, and `ib.pnl()` provides real-time profit and loss information.
-   **[ADK_IMPLEMENTATION]** A `FunctionTool` called `get_portfolio_state` will be created. This tool will be called by the Risk Governor callback before any new trade to check for things like max portfolio heat, sector concentration, and current drawdown.

```python
# Example: Fetching portfolio and P&L
portfolio = ib.portfolio()
for position in portfolio:
    print(f"Position: {position.contract.symbol}, Quantity: {position.position}")

pnl = ib.pnl()
print(f"Realized P&L: {pnl.realizedPnl}, Unrealized P&L: {pnl.unrealizedPnl}")
```

### [USE_CASE: Data_and_Execution] Combining EODHD and IBKR

Our agent will leverage both APIs in a complementary fashion:

1.  **Signal Generation (EODHD):** The agent will use the EODHD WebSocket for real-time data to power its indicators and generate trading signals. This offloads the high-volume data stream from our execution gateway.
2.  **Pre-Execution Verification (IBKR):** Just before placing an order, the agent can make a final price check using `ib.reqMktData()` to get a high-fidelity quote from the execution venue itself.
3.  **Execution (IBKR):** All orders are placed, managed, and monitored through the IBKR API.

This hybrid approach uses each provider for its core strength: EODHD for broad, cost-effective data coverage, and IBKR for robust, low-latency trade execution and account management.

[SOURCE_ID: Interactive Brokers API Python Documentation, ib_insync Documentation]
