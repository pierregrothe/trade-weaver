# File: /trade_weaver/sub_agents/market_analyst/tools.py
"""
Defines the tools available to the Market Analyst agent.

These tools are responsible for interacting with external data sources (like APIs)
and internal systems (like databases) to gather the necessary information for
market regime analysis and to persist the results.
"""
import logging
from datetime import datetime
import pytz
from google.adk.tools import FunctionTool, ToolContext

# --- Tool Implementations ---

def get_vix_data() -> dict:
    """
    Retrieves the current CBOE Volatility Index (VIX) value.

    This tool is a critical first step for assessing overall market fear and
    investor sentiment.

    Returns:
        A dictionary containing the status and the VIX value.
        Example: {"status": "success", "vix_value": 22.5, "timestamp": "..."}
    """
    logging.info("Tool: get_vix_data called. Returning mock data.")
    return {
        "status": "success",
        "vix_value": 22.5,
        "timestamp": datetime.utcnow().isoformat()
    }

def get_adx_data(tool_context: ToolContext) -> dict:
    """
    Retrieves the Average Directional Index (ADX) for a given market proxy.

    This tool measures the strength of the current market trend. It requires
    the 'market_proxy' and 'adx_period' to be present in the session state.

    Args:
        tool_context: The context object providing access to session state.

    Returns:
        A dictionary containing the status and the ADX value.
        Example: {"status": "success", "adx_value": 28.1, "timestamp": "..."}
    """
    market_proxy = tool_context.state.get("market_proxy", "UNKNOWN")
    adx_period = tool_context.state.get("adx_period", 14)
    logging.info(
        f"Tool: get_adx_data called for {market_proxy} with period {adx_period}. "
        "Returning mock data."
    )
    return {
        "status": "success",
        "adx_value": 28.1,
        "timestamp": datetime.utcnow().isoformat()
    }

def get_current_time() -> dict:
    """
    Gets the current time in the 'America/New_York' timezone.

    This is essential for determining the time-of-day state of the market,
    which influences trading strategy selection (e.g., Opening Hour vs.
    Midday Lull).

    Returns:
        A dictionary containing the current time in ISO 8601 format.
    """
    logging.info("Tool: get_current_time called.")
    ny_timezone = pytz.timezone("America/New_York")
    ny_time = datetime.now(ny_timezone)
    return {"current_time_iso": ny_time.isoformat()}

def persist_market_regime(tool_context: ToolContext) -> dict:
    """
    Persists the final, validated market regime state to a data store.

    This is the final step in the agent's workflow. It reads the analysis
    result from the 'intermediate_market_regime' key in the session state
    and logs it for persistence. In a real implementation, this would write
    to a database like Firestore.

    Args:
        tool_context: The context object providing access to session state.

    Returns:
        A dictionary confirming the persistence status.
    """
    market_regime_data = tool_context.state.get("intermediate_market_regime")
    if not market_regime_data:
        logging.error("Tool Error: 'intermediate_market_regime' not found in state.")
        return {"status": "error", "message": "No market regime data to persist."}

    # In a real scenario, this would be a database write operation.
    # For now, we just log the action.
    logging.info(f"Persisting market regime to data store: {market_regime_data}")

    return {"status": "success", "persisted": True}


# --- Tool Registration ---
# The ADK automatically wraps functions passed in a tools list into FunctionTools.
# The function's docstring is used as its description for the LLM.
market_analyst_tools = [
    get_vix_data,
    get_adx_data,
    get_current_time,
    persist_market_regime,
]
