from google.adk.agents import LlmAgent

from ..config import FLASH_MODEL
from ..utils.logging_callbacks import log_agent_entry, log_agent_exit

post_market_journaling_agent = LlmAgent(
    name="post_market_journaling_agent",
    model=FLASH_MODEL,
    description="Analyzes the day's trades and generates a performance journal.",
    instruction="""Your task is to perform post-market analysis.
    1. Load the 'executed_trades' from the session state.
    2. Calculate key performance metrics (e.g., win rate, profit factor).
    3. Generate a summary of the trading day.
    4. Store the journal entry in the session state under the key 'daily_journal'.""",
    output_key="daily_journal",
    before_agent_callback=log_agent_entry,
    after_agent_callback=log_agent_exit,
)