# [TOOL: API_Playbook] API Playbook for EODHD and Interactive Brokers

This document is a detailed, practical guide for developers building the tools that interact with our primary external APIs. It provides code examples and best practices for the two pillars of our external interactions:

1.  **EOD Historical Data (EODHD):** Our primary source for all market data, including historical, fundamental, and real-time streams.
2.  **Interactive Brokers (IBKR):** Our primary venue for all trade execution and portfolio management.

## 1. EODHD API (`eodhd` library)

We use the official `eodhd` Python library for all interactions with EODHD.

### Use Case 1: Fetching Historical Data

**Purpose:** To populate our analytical database (BigQuery) for backtesting and to provide historical context to our agents.

```python
from eodhd import APIClient

# It is highly recommended to use environment variables for API keys
API_KEY = "YOUR_EODHD_API_KEY"
client = APIClient(API_KEY)

# Get daily historical data for a stock
historical_data = client.get_historical_data(
    symbol="AAPL.US",
    interval="d" # "d" for daily, "m" for monthly
)

# Get 1-minute intraday historical data
intraday_data = client.get_intraday_historical_data(
    symbol="AAPL.US",
    interval="1m"
)
```

### Use Case 2: Real-Time Data Streaming (WebSocket)

**Purpose:** To power the live `Data Ingestion Service`. This service will connect to the WebSocket and broadcast all received messages to a GCP Pub/Sub topic for consumption by the agents.

```python
import asyncio
from eodhd import APIClient

API_KEY = "YOUR_EODHD_API_KEY"

async def stream_market_data():
    """Connects to the EODHD WebSocket and streams trades for specified symbols."""
    client = APIClient(API_KEY)
    symbols = ["AAPL.US", "MSFT.US"]

    def on_message(message):
        """In production, this function would publish the message to GCP Pub/Sub."""
        print(f"Received trade: {message}")

    ws_client = client.new_websocket_client(
        endpoint="us", on_message_callback=on_message
    )
    await ws_client.run_async()

# To run this: asyncio.run(stream_market_data())
```

### Use Case 3: Fetching News & Fundamentals

**Purpose:** A critical component for the `MarketAnalystAgent` to enrich potential trading candidates with catalyst information.

```python
from eodhd import APIClient

API_KEY = "YOUR_EODHD_API_KEY"
client = APIClient(API_KEY)

# Get fundamental data for a company
fundamentals = client.get_fundamental_equity("MSFT.US")

# Get recent financial news
news = client.get_financial_news_and_sentiment_data(s="MSFT.US")
```

## 2. Interactive Brokers API (`ib_insync` library)

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
