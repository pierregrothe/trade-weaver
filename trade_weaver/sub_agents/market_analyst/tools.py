"""
Defines the state-driven tools for the Market Analyst agent pipeline.

This module provides the building blocks for the SequentialAgent, where each
tool is designed to be driven by and contribute to the session state.
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

# --- 1. Individual, State-Driven Tool Implementations ---


def get_exchange_details(exchange: str, tool_context: ToolContext) -> dict:
    """
    Simulates fetching exchange details from a database.
    In a real scenario, this would query Firestore or another data source.
    For this implementation, it returns hardcoded data for known exchanges.
    The entire returned dictionary will be placed into the 'exchange_details' state key.
    """
    logging.info(f"Tool: get_exchange_details called for '{exchange}'.")
    # Data derived from the provided screenshot in the project plan.
    exchange_data = {
        "NASDAQ": {
            "timezone": "America/New_York",
            "market_proxy": "QQQ",
            "volatility_index": "^VIX",
            "yfinance_suffix": ".US",
        },
        "NYSE": {
            "timezone": "America/New_York",
            "market_proxy": "SPY",
            "volatility_index": "^VIX",
            "yfinance_suffix": ".US",
        },
    }
    details = exchange_data.get(exchange)
    if details:
        tool_context.state["exchange_details"] = details
        return details
    else:
        # This will cause a downstream error, which is a valid outcome for a
        # non-existent exchange.
        return {"error": f"Exchange '{exchange}' not found."}


def get_vix_data(tool_context: ToolContext) -> dict:
    """
    Retrieves the current CBOE Volatility Index (VIX) value.
    It reads the 'volatility_index' from the 'exchange_details' in the session state.
    The returned dictionary will be placed into the 'vix_data' state key.
    """
    exchange_details = tool_context.state.get("exchange_details")
    if not exchange_details or "volatility_index" not in exchange_details:
        msg = "get_vix_data requires 'exchange_details' with a 'volatility_index' key."
        logging.error(f"TOOL ERROR: {msg}")
        return {"status": "error", "message": msg}

    volatility_index = exchange_details["volatility_index"]
    logging.info(f"Tool: get_vix_data called for {volatility_index}. Returning mock data.")
    result = {"vix_value": 22.5}
    tool_context.state["vix_data"] = result
    return result


def get_adx_data(tool_context: ToolContext) -> dict:
    """
    Retrieves the Average Directional Index (ADX) for a given market proxy.
    It reads the 'market_proxy' from 'exchange_details' in the session state.
    The returned dictionary will be placed into the 'adx_data' state key.
    """
    exchange_details = tool_context.state.get("exchange_details")
    if not exchange_details or "market_proxy" not in exchange_details:
        msg = "get_adx_data requires 'exchange_details' with a 'market_proxy' key."
        logging.error(f"TOOL ERROR: {msg}")
        return {"status": "error", "message": msg}

    market_proxy = exchange_details["market_proxy"]
    logging.info(f"Tool: get_adx_data called for {market_proxy}. Returning mock data.")
    result = {"adx_value": 28.1}
    tool_context.state["adx_data"] = result
    return result


def get_current_time(tool_context: ToolContext) -> dict:
    """
    Gets the current time in the timezone specified by the exchange details.
    The returned dictionary will be placed into the 'time_data' state key.
    """
    exchange_details = tool_context.state.get("exchange_details")
    if not exchange_details or "timezone" not in exchange_details:
        msg = "get_current_time requires 'exchange_details' with a 'timezone' key."
        logging.error(f"TOOL ERROR: {msg}")
        return {"status": "error", "message": msg}

    try:
        tz_str = exchange_details["timezone"]
        exchange_timezone = pytz.timezone(tz_str)
        exchange_time = datetime.now(exchange_timezone)
        result = {"current_time_iso": exchange_time.isoformat()}
        tool_context.state["time_data"] = result
        return result
    except pytz.UnknownTimeZoneError:
        logging.error(f"TOOL ERROR: Invalid timezone '{tz_str}' provided.")
        return {"status": "error", "message": f"Invalid timezone: {tz_str}"}


def persist_market_regime(tool_context: ToolContext) -> dict:
    """
    Persists the final, validated market regime state to a data store.
    It reads the analysis result from the 'validated_market_regime' key
    in the session state and logs it for persistence.
    """
    market_regime_data = tool_context.state.get("validated_market_regime")
    if not market_regime_data:
        msg = "'validated_market_regime' not found in state."
        logging.error(f"TOOL ERROR: persist_market_regime called but {msg}")
        return {"status": "error", "message": f"Critical error: {msg}"}

    logging.info(f"PERSISTENCE: Storing market regime in data store: {market_regime_data}")
    return {"status": "success", "persisted": True}


# --- Mock Stock Scanning Tools ---

def find_pre_market_movers(tool_context: ToolContext) -> dict:
    """Simulates finding top pre-market movers for the given exchange."""
    exchange = tool_context.state.get("exchange_details", {}).get("market_proxy", "UNKNOWN")
    logging.info(f"Tool: find_pre_market_movers for {exchange}. Returning mock tickers.")
    result = {"tickers": ["MSFT", "GOOG", "TSLA"]}
    tool_context.state["pre_market_movers"] = result
    return result

def get_full_stock_details(tool_context: ToolContext, ticker: str) -> dict:
    """
    Simulates fetching a consolidated set of details for a single stock ticker,
    including profile, financial data, and news. This is more efficient than
    calling three separate tools.
    """
    logging.info(f"Tool: get_full_stock_details for {ticker}. Returning mock data.")

    # Combine profile, financials, and news into one payload
    details = {
        "profile": {
            "sector": "Technology",
            "industry": "Software - Infrastructure",
            "market_cap": 2_000_000_000_000,
        },
        "financials": {
            "adjusted_close": 305.00,
            "pre_market_high": 308.50,
            "pre_market_low": 304.00,
        },
        "news": [
            {"headline": "New AI Product Announced", "source": "Reuters", "timestamp": datetime.now().isoformat()}
        ]
    }

    # Store the consolidated details in the state
    if "full_stock_details" not in tool_context.state:
        tool_context.state["full_stock_details"] = {}
    tool_context.state["full_stock_details"][ticker] = details

    return {"status": "success", "ticker": ticker, "details": details}


# --- 2. Create the Toolset with State-Aware Tools ---


class MarketAnalystToolset(BaseToolset):
    """A toolset that encapsulates all tools for the market analysis pipeline."""

    def __init__(self, prefix: str = "market_"):
        self.prefix = prefix

        # Instantiate each function as a FunctionTool.
        self.get_exchange_details_tool = FunctionTool(func=get_exchange_details)
        self.get_vix_data_tool = FunctionTool(func=get_vix_data)
        self.get_adx_data_tool = FunctionTool(func=get_adx_data)
        self.get_current_time_tool = FunctionTool(func=get_current_time)
        self.persist_market_regime_tool = FunctionTool(func=persist_market_regime)

        # Stock scanning tools
        self.find_pre_market_movers_tool = FunctionTool(func=find_pre_market_movers)
        self.get_full_stock_details_tool = FunctionTool(func=get_full_stock_details)


    async def get_tools(
        self, readonly_context: Optional[ReadonlyContext] = None
    ) -> List[BaseTool]:
        """Return all market regime and stock scanning tools."""
        return [
            self.get_exchange_details_tool,
            self.get_vix_data_tool,
            self.get_adx_data_tool,
            self.get_current_time_tool,
            self.persist_market_regime_tool,
            self.find_pre_market_movers_tool,
            self.get_full_stock_details_tool,
        ]

    async def close(self) -> None:
        """Cleans up any resources held by the toolset."""
        await asyncio.sleep(0)  # Placeholder for async cleanup


# --- 3. Instantiate and Export the Toolset ---
market_analyst_toolset = MarketAnalystToolset()