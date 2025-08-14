# [TOOL: EODHD_Playbook] EODHD API Playbook

This document is a detailed, practical guide for developers on using the EOD Historical Data (EODHD) API, which is our primary source for all market data.

We use the official `eodhd` Python library for all interactions.

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
