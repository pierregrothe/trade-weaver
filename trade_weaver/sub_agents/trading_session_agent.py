from google.adk.agents import LlmAgent

from ..config import FLASH_MODEL
from ..utils.logging_callbacks import log_agent_entry, log_agent_exit

# In a real implementation, this might be a LoopAgent that runs until market close.
trading_session_agent = LlmAgent(
    name="trading_session_agent",
    model=FLASH_MODEL,
    description="Executes trades based on the daily watchlist and market conditions.",
    instruction="""Your task is to manage the trading session.
    1. Load the 'daily_watchlist' from the session state.
    2. Monitor real-time market data for entry signals on watchlist stocks.
    3. Execute trades according to the defined strategy (e.g., Opening Range Breakout).
    4. Manage open positions with defined stop-loss and take-profit rules.
    5. Store all executed trades in the session state under the key 'executed_trades'.""",
    output_key="trading_session_summary",
    before_agent_callback=log_agent_entry,
    after_agent_callback=log_agent_exit,
)