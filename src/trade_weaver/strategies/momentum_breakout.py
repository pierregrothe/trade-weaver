# File: src/trade_weaver/strategies/momentum_breakout.py

def run(market_data: dict) -> dict | None:
    """
    Analyzes market data for a simple momentum breakout opportunity.

    Args:
        market_data (dict): A dictionary containing the latest market data,
                            including a 'last_price' key.

    Returns:
        A dictionary representing a trade opportunity if the breakout condition is met,
        otherwise None.
    """
    ticker = market_data.get("ticker", "UNKNOWN")
    current_price = market_data.get("last_price")
    breakout_level = 152.00  # We'll make this dynamic in a future step

    print(f"STRATEGY(Momentum_Breakout): Analyzing {ticker} at price ${current_price} against level ${breakout_level}")

    if current_price and current_price > breakout_level:
        opportunity = {
            "ticker": ticker,
            "strategy": "Momentum_Breakout_v1",
            "direction": "LONG",
            "entry_price": breakout_level + 0.01, # Enter just above the breakout
            "stop_loss": breakout_level - 0.50,
            "target_price": breakout_level + 3.00,
            "confidence_score": 0.85
        }
        print(f"STRATEGY(Momentum_Breakout): --> OPPORTUNITY FOUND for {ticker}")
        return opportunity
    
    print(f"STRATEGY(Momentum_Breakout): --> No opportunity found for {ticker}")
    return None