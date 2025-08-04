# File: src/trade_weaver/tools/market_data_tools.py (Corrected)

from trade_weaver.core.ibkr_broker import IBKRBroker

def get_market_data(ticker: str) -> dict:
    """
    Connects to the broker and retrieves market data for a given stock ticker.

    Args:
        ticker (str): The stock symbol (e.g., "NVDA", "AAPL").

    Returns:
        dict: A dictionary with 'status' and the 'price' if successful.
    """
    print(f"TOOL INFO: 'get_market_data' tool invoked for ticker: {ticker}")
    broker = IBKRBroker()
    
    if broker.connect(portfolio_id="simulated_portfolio"):
        response = broker.get_market_data(ticker)
        broker.disconnect()
        
        if response.get("status") == "success":
            price = response.get("data", {}).get("last_price")
            # Return a simple, structured dictionary. This is the preferred pattern.
            return {"status": "success", "price": price}
        else:
            return {"status": "error", "message": response.get("message", "Broker error")}
    else:
        return {"status": "error", "message": "Could not connect to the broker."}