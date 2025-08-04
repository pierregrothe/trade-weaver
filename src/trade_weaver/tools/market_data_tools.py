# File: src/trade_weaver/tools/market_data_tools.py

from trade_weaver.core.ibkr_broker import IBKRBroker
# In the future, we might add a factory here to select the right broker.

def get_market_data(ticker: str) -> dict:
    """
    Connects to the broker and retrieves the latest market data for a given stock ticker.

    Args:
        ticker (str): The stock symbol (e.g., "NVDA", "AAPL").

    Returns:
        dict: A dictionary containing the market data from the broker.
    """
    print(f"TOOL INFO: 'get_market_data' tool invoked for ticker: {ticker}")
    broker = IBKRBroker()
    
    # In a real app, portfolio_id would come from the ToolContext
    if broker.connect(portfolio_id="simulated_portfolio"):
        market_data = broker.get_market_data(ticker)
        broker.disconnect()
        return market_data
    else:
        return {"status": "error", "message": "Could not connect to the broker."}