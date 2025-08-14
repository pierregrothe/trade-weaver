# [TOOL: IBKR_Playbook] Interactive Brokers API Playbook

This document is a detailed, practical guide for developers on using the Interactive Brokers (IBKR) API, which is our primary venue for all trade execution and portfolio management.

We use the `ib_insync` library for its robust, asynchronous interface to the IBKR Trader Workstation (TWS) or IB Gateway API.

### Use Case 1: Placing an Advanced Bracket Order

**Purpose:** This is the standard method for the `ExecutionAgent` to enter a trade. It ensures every position is immediately protected with a stop-loss and has a defined profit target, enforcing discipline programmatically.

```python
from ib_insync import *

# util.startLoop() is required for standalone scripts.
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1) # Connect to TWS or Gateway

# 1. Define the contract
contract = Stock('TSLA', 'SMART', 'USD')
ib.qualifyContracts(contract)

# 2. Create the three-part bracket order
bracket_order = ib.bracketOrder(
    action='BUY',
    quantity=10,
    limitPrice=175.00,       # Entry price
    takeProfitPrice=180.00,  # Profit target
    stopLossPrice=172.50     # Stop-loss
)

# 3. Place all three linked orders
for order in bracket_order:
    trade = ib.placeOrder(contract, order)
    print(f"Placed Order: {trade.order.action} {trade.order.totalQuantity} {contract.symbol}")

ib.run() # Keep connection alive
```

### Use Case 2: Real-Time Portfolio Monitoring

**Purpose:** To provide the `RiskGovernor` with a real-time view of the portfolio's state (positions, P&L) before approving any new trade.

```python
from ib_insync import *

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)

# Fetch all positions in the account
positions = ib.portfolio()
for position in positions:
    print(f"Holding {position.position} shares of {position.contract.symbol}")

# Fetch real-time Profit and Loss
pnl = ib.pnl()
print(f"Unrealized P&L: {pnl.unrealizedPnl}, Realized P&L: {pnl.realizedPnl}")

ib.disconnect()
```
