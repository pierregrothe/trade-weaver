from google.adk.agents import LlmAgent

from ..config import FLASH_MODEL
from ..utils.logging_callbacks import log_agent_entry, log_agent_exit

pre_market_scanner_agent = LlmAgent(
    name="pre_market_scanner_agent",
    model=FLASH_MODEL,
    description="Scans for pre-market gappers and news catalysts to build a daily watchlist.",
    instruction="""Your task is to perform pre-market analysis.
    1. Identify stocks with significant pre-market price gaps and high relative volume.
    2. Find any news catalysts associated with these stocks.
    3. Create a ranked watchlist based on this analysis.
    4. Store the final watchlist in the session state under the key 'daily_watchlist'.""",
    output_key="daily_watchlist",
    before_agent_callback=log_agent_entry,
    after_agent_callback=log_agent_exit,
)