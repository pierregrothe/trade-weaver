# API Usage Playbook

This document provides practical, build-ready Python code examples for interacting with the primary external APIs used in the Trade Weaver platform. The philosophy is to use **EODHD for data** and **Interactive Brokers for execution**.

## 1. EODHD: Real-Time Data Streaming

This playbook uses the official `eodhd` Python library to connect to the EODHD WebSocket for real-time data. This is the primary method for ingesting the live market data that powers the agent's signals.

**Use Case:** A dedicated data ingestion service (running on Cloud Run) will execute this code to stream data and publish it to a GCP Pub/Sub topic.

```python
# Ensure the library is installed: pip install eodhd
import asyncio
from eodhd import APIClient

# It is highly recommended to use environment variables for API keys
API_KEY = "YOUR_EODHD_API_KEY"

async def main():
    """Connects to the EODHD WebSocket and streams trades for specified symbols."""
    client = APIClient(API_KEY)
    
    # Define the symbols to subscribe to for US stocks
    symbols = ["AAPL.US", "MSFT.US"]

    def on_message(message):
        """
        Callback function to process incoming messages.
        In a real implementation, this would publish the message to Pub/Sub.
        """
        print(f"Received trade: {message}")

    # Get a new WebSocket client for the 'us' endpoint
    ws_client = client.new_websocket_client(
        endpoint="us",
        on_message_callback=on_message
    )

    # Run the client asynchronously
    await ws_client.run_async()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated by user.")

```

## 2. Interactive Brokers: Trade Execution

This playbook uses the `ib_insync` library to connect to the Interactive Brokers TWS or Gateway and place a trade. This is the primary method for all trade execution and order management.

**Use Case:** An `execute_trade` FunctionTool within the execution agent will wrap this logic to place orders based on the agent's decisions.

```python
# Ensure the library is installed: pip install ib_insync
from ib_insync import *

# util.startLoop() is required for standalone scripts to run the event loop.
util.startLoop()

ib = IB()
try:
    # Connect to a running TWS or IB Gateway instance
    ib.connect('127.0.0.1', 7497, clientId=1)

    # 1. Define the contract for the instrument to trade
    contract = Stock('TSLA', 'SMART', 'USD')
    ib.qualifyContracts(contract) # Recommended to get full contract details

    # 2. Define the order (e.g., a bracket order for entry, profit, and stop-loss)
    # This order buys 10 shares at a limit price of $175,
    # with a take-profit at $180 and a stop-loss at $172.50.
    bracket_order = ib.bracketOrder(
        action='BUY',
        quantity=10,
        limitPrice=175.00,
        takeProfitPrice=180.00,
        stopLossPrice=172.50
    )

    # 3. Place the order
    # The bracketOrder returns a list of three orders (parent, take-profit, stop-loss)
    for order in bracket_order:
        trade = ib.placeOrder(contract, order)
        print(f"Placed Order: {trade.order.action} {trade.order.totalQuantity} {contract.symbol}")
        print(f"Order Status: {trade.orderStatus.status}")

    # ib.run() will block and keep the script running to receive updates
    ib.run()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if ib.isConnected():
        ib.disconnect()

```
