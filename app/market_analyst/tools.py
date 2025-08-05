# app/market_analyst/tools.py
from app.config import EODHD_API_KEY
from eodhd import APIClient
from pydantic import BaseModel, Field
from google.adk.tools import FunctionTool

# --- Tool Input Schema ---
class ScreenerInput(BaseModel):
    exchange: str = Field(default="US", description="The stock exchange to screen (e.g., 'US', 'LSE', 'TSE').")
    min_price: float = Field(default=5.0, description="The minimum price of stocks to include.")
    max_price: float = Field(default=100.0, description="The maximum price of stocks to include.")
    min_volume: int = Field(default=500000, description="The minimum average daily volume.")
    min_gap_percent: float = Field(default=4.0, description="The minimum pre-market gap percentage to identify.")

# --- EODHD API Tool ---
async def screen_for_gappers(
    exchange: str = "US",
    min_price: float = 5.0,
    max_price: float = 100.0,
    min_volume: int = 500000,
    min_gap_percent: float = 4.0
) -> str:
    """
    Screens a given stock exchange for pre-market gappers using the EODHD API.
    A 'gapper' is a stock whose price has changed significantly from the previous day's close.

    Args:
        exchange: The stock exchange to screen.
        min_price: The minimum price of stocks to include.
        max_price: The maximum price of stocks to include.
        min_volume: The minimum average daily volume.
        min_gap_percent: The minimum gap percentage to identify.

    Returns:
        A JSON string containing a list of potential gapper stocks with their details,
        or an error message if the screening fails.
    """
    try:
        async with APIClient(EODHD_API_KEY) as client:
            # The EODHD screener API is a good proxy for finding gappers.
            # We filter by volume, price, and a positive change to find stocks moving up.
            screener_payload = {
                "filters": [
                    ["exchange", "=", exchange],
                    ["avgvol_d", ">", min_volume],
                    ["close", "between", [min_price, max_price]],
                    ["change_p", ">", min_gap_percent] # Stocks that have already gapped up
                ],
                "sort": ["change_p", "desc"],
                "limit": 10
            }
            
            response = await client.screener(payload=screener_payload)
            
            if response and "data" in response and response["data"]:
                return str(response["data"])
            else:
                return "No gappers found matching the criteria."

    except Exception as e:
        return f"An error occurred while screening for gappers: {e}"

# --- Create FunctionTool ---
screen_exchanges_tool = FunctionTool(
    func=screen_for_gappers,
    input_schema=ScreenerInput,
    description="Screens stock exchanges to find potential pre-market gappers based on price, volume, and gap percentage."
)
