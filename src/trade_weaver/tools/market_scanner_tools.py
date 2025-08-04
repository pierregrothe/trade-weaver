# File: src/trade_weaver/tools/market_scanner_tools.py (Corrected)

def create_tradable_universe() -> dict:
    """
    Scans the entire market to filter for stocks that are fundamentally suitable for day trading.
    This filter is based on minimum liquidity, price, and volatility criteria.
    It should be run once daily to generate the base list for pre-market scanning.

    Returns:
        dict: A dictionary containing the status and a list of tickers in the tradable universe.
    """
    print("TOOL INFO: 'create_tradable_universe' tool invoked.")
    # In a real implementation, this would connect to a market data provider.
    # For now, we will return a hardcoded list of typically high-volume, volatile stocks.
    mock_universe = ["AAPL", "GOOG", "NVDA", "TSLA", "AMD", "MSFT", "META"]
    
    print(f"TOOL INFO: Found {len(mock_universe)} stocks for the Tradable Universe.")
    return {"status": "success", "tradable_universe": mock_universe}