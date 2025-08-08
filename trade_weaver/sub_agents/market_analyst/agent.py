"""
Defines the Market Analyst Agent, its callbacks, and its instantiation.

This agent is responsible for analyzing market conditions (volatility, trend, time)
and producing a structured `MarketRegimeState` object. It leverages ADK callbacks
for robust logging, validation, and state management.
"""

import json
import logging
import re
from typing import Dict, Any, Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool
from pydantic import ValidationError

from trade_weaver.config import MODEL_FLASH
from .prompt import INSTRUCTION
from .schemas import MarketRegimeState
from .tools import MarketAnalystToolset

market_toolset = MarketAnalystToolset()

# --- ADK Callbacks for Robustness and Observability ---
def validate_and_log_tool_output(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    """
    ADK `after_tool_callback` to perform structured logging and basic validation.
    """
    tool_name = tool.name

    # Structured logging for better observability
    log_data: Dict[str, Any] = {
        "event": "after_tool_call",
        "tool_name": tool_name,
        "tool_args": args,
        "tool_response": tool_response,
        # VALIDATED: This explicit path is robust and satisfies static analysis.
        "session_id": tool_context._invocation_context.session.id,
    }
    logging.info(json.dumps(log_data))

    # Basic validation for critical data points
    if tool_name == "get_vix_data":
        if isinstance(tool_response, dict):
            vix_value = tool_response.get("vix_value", -1.0)
            if not isinstance(vix_value, (int, float)) or vix_value < 0:
                logging.warning(f"VIX value '{vix_value}' is unrealistic.")

    if tool_name == "get_adx_data":
        if isinstance(tool_response, dict):
            adx_value = tool_response.get("adx_value", -1.0)
            if not isinstance(adx_value, (int, float)) or adx_value < 0:
                logging.warning(f"ADX value '{adx_value}' is unrealistic.")
    
    # Return None to indicate no modification of the tool_response is needed.
    return None


def parse_and_save_intermediate_state(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """
    ADK `after_model_callback` to parse, validate, and save structured state.

    This is a critical data integrity step. It finds the JSON block in the LLM's
    text response, validates it against the `MarketRegimeState` Pydantic schema,
    and if successful, saves the structured data to the session state. This makes
    the validated data available to subsequent tools like `persist_market_regime`.
    """
    if not (llm_response and llm_response.content and llm_response.content.parts):
        logging.debug("after_model_callback: LlmResponse has no content to parse.")
        return None

    model_response_text = "".join(
        part.text for part in llm_response.content.parts if part.text
    )
    
    log_data: Dict[str, Any] = {
        "event": "after_model_call",
        "session_id": callback_context._invocation_context.session.id,
    }

    try:
        # Use a resilient regex to find a JSON object within the text
        match = re.search(r"\{.*\}", model_response_text, re.DOTALL)
        if not match:
            raise json.JSONDecodeError("No JSON object found in response.", model_response_text, 0)
        
        json_str = match.group(0)
        json_data = json.loads(json_str)
        validated_data = MarketRegimeState(**json_data)

        callback_context.state["intermediate_market_regime"] = validated_data.model_dump()
        
        log_data["status"] = "success"
        log_data["validated_data"] = validated_data.model_dump()

    except (json.JSONDecodeError, ValidationError) as e:
        log_data["status"] = "error"
        log_data["error_message"] = str(e)
        logging.error(f"Failed to parse or validate market regime state: {e}")

    logging.info(json.dumps(log_data, indent=2))
    
    # Return None to indicate no modification of the LlmResponse is needed.
    return None

# --- Agent Definition ---
market_analyst_agent = LlmAgent(
    name="market_analyst_agent",
    description="Analyzes and reports on the current market regime.",
    model=MODEL_FLASH,
    instruction=INSTRUCTION,
    tools=[market_toolset],
    after_tool_callback=validate_and_log_tool_output,
    after_model_callback=parse_and_save_intermediate_state,
    output_key="intermediate_market_regime",

)