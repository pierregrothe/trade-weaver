# [TOOL: EODHD_API] EODHD API Playbook

This document provides a practical guide for using the EOD Historical Data (EODHD) API to power the data ingestion and analysis modules of the AI trading agent. We will use the official `eodhd` Python library.

### [PRINCIPLE: Role_in_Architecture] EODHD's Role in the System Architecture

EODHD will serve as our primary data provider for a broad range of historical and fundamental data, as well as for real-time data streaming via WebSockets. Its strength lies in its consolidated, easy-to-use API that covers multiple asset classes.

### [IMPLEMENTATION: Python_Library] Using the `eodhd` Python Library

All interactions with the EODHD API will be done through the official `eodhd` Python library. This ensures maintainability and access to the latest features.

```python
# Basic setup
from eodhd import APIClient

# The API key should be stored as an environment variable
api_key = "YOUR_EODHD_API_KEY"
client = APIClient(api_key)
```

### [USE_CASE: Real_Time_Data] 1. Real-Time Data Streaming (WebSocket)

For a day trading agent, a persistent, low-latency WebSocket connection is mandatory for receiving real-time trade data.

- **[HOW]** We will use the library's `EODHDClient.new_websocket_client()` method to establish the connection. The client will run in a separate, asynchronous thread to avoid blocking the main application.
- **[ADK_IMPLEMENTATION]** A dedicated data ingestion service (e.g., a GCP Cloud Run instance) will run this WebSocket client. It will receive messages and publish them to a GCP Pub/Sub topic, from which the main trading agent can subscribe. This decouples data ingestion from trading logic.

```python
# Example: Real-time trade data for multiple stocks
def on_message(message):
    print(f"Received trade: {message}")
    # In production, this would publish the message to a Pub/Sub topic

ws_client = client.new_websocket_client(
    endpoint="us",
    on_message_callback=on_message,
    symbols=["AAPL.US", "MSFT.US"]
)
ws_client.run_async() # Runs the client in a background thread
```

### [USE_CASE: Technical_Indicators] 2. Offloading Technical Indicator Calculations

EODHD provides an API endpoint to calculate a wide range of technical indicators. This allows us to offload the computational work from our agent.

- **[HOW]** The `client.get_technical_indicator_data()` method can be used to request pre-calculated indicator values.
- **[ADK_IMPLEMENTATION]** A `FunctionTool` within the agent can call this endpoint on demand to get up-to-date indicator values for a given stock, which can then be used as features for the agent's decision-making process.

```python
# Example: Get the 14-day RSI for AAPL
rsi_data = client.get_technical_indicator_data(
    symbol="AAPL.US",
    function="rsi",
    period=14
)
```

### [USE_CASE: News_and_Sentiment] 3. News and Sentiment Analysis

EODHD provides a news API with sentiment analysis, which is a critical input for our catalyst-driven strategies.

- **[HOW]** The `client.get_financial_news_and_sentiment_data()` method can be used to retrieve recent news headlines and their associated sentiment scores.
- **[ADK_IMPLEMENTATION]** This will be a core component of our pre-market scanning pipeline. A `FunctionTool` will call this endpoint for stocks on our potential watchlist to get a quantitative measure of the news catalyst, which will be used in our Gapper Quality Score (GQS).

```python
# Example: Get news and sentiment for AAPL
news_data = client.get_financial_news_and_sentiment_data(
    s="AAPL.US",
    from_date="2024-01-01"
)
```

### [USE_CASE: What_to_Build] What We Still Need to Build

While EODHD provides a wealth of data, it does not cover everything. We will need to build the following components from scratch:

- **Advanced AI/ML Models:** EODHD provides the raw data, but we are responsible for building, training, and deploying our own LSTM, Reinforcement Learning, and other advanced predictive models.
- **Custom Feature Engineering:** While EODHD offers standard technical indicators, any proprietary or complex features (like Order Flow Imbalance) will need to be calculated by our agent.
- **The Core Trading Logic:** The agent's decision-making matrix, risk management rules, and overall trading logic are unique to our system and must be built internally.

[SOURCE_ID: EODHD API Documentation]
