"""
Defines the tools available to the Market Analyst agent, organized within a Toolset.

This module encapsulates all data gathering and persistence logic into a
single, manageable MarketAnalystToolset class, following ADK best practices for
organizing related tools.
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Optional

import pytz
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools import FunctionTool, ToolContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.base_toolset import BaseToolset

# --- 1. Individual Tool Function Implementations ---
# (The underlying logic of your functions remains unchanged as it is already excellent)

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
    # In a real implementation, this would call the EODHD API.
    return {
        "status": "success",
        "vix_value": 22.5,
        "timestamp": datetime.now(pytz.UTC).isoformat()
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
        "timestamp": datetime.now(pytz.UTC).isoformat()
    }

def get_current_time() -> dict:
    """
    Gets the current time in the 'America/New_York' timezone.
    This is essential for determining the time-of-day state of the market.

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
    It reads the analysis result from the 'intermediate_market_regime' key
    in the session state and logs it for persistence.

    Args:
        tool_context: The context object providing access to session state.

    Returns:
        A dictionary confirming the persistence status.
    """
    market_regime_data = tool_context.state.get("intermediate_market_regime")
    if not market_regime_data:
        logging.error("TOOL ERROR: persist_market_regime called but 'intermediate_market_regime' was not found in the session state.")
        return {"status": "error", "message": "Critical error: No market regime data was found in the state to persist."}

    logging.info(f"Persisting market regime to data store: {market_regime_data}")
    return {"status": "success", "persisted": True}


# --- 2. Create the Toolset (ADK Best Practice) ---

class MarketAnalystToolset(BaseToolset):
    """A toolset that encapsulates all tools for market regime analysis."""

    def __init__(self, prefix: str = "market_"):
        self.prefix = prefix

        self._get_vix_data_tool = FunctionTool(func=get_vix_data)
        self._get_adx_data_tool = FunctionTool(func=get_adx_data)
        self._get_current_time_tool = FunctionTool(func=get_current_time)
        self._persist_market_regime_tool = FunctionTool(func=persist_market_regime)
        
    async def get_tools(self, readonly_context: Optional[ReadonlyContext] = None) -> List[BaseTool]:
        """Return all market regime tools."""
        tools = [
            self._get_vix_data_tool,
            self._get_adx_data_tool,
            self._get_current_time_tool,
            self._persist_market_regime_tool            
        ]
        
        return tools

    async def close(self) -> None:
        """
        Cleans up any resources held by the toolset.
        (No resources to clean up in this mock implementation).
        """
        await asyncio.sleep(0) # Placeholder for async cleanup if needed


# --- 3. Instantiate and Export the Toolset ---
# This single instance will be imported and used by the agent.
market_analyst_toolset = MarketAnalystToolset()