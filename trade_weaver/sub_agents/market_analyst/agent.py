# File: /trade_weaver/sub_agents/market_analyst/agent.py
"""
Defines the Market Analyst Agent, its callbacks, and its instantiation.

This agent is responsible for analyzing market conditions (volatility, trend, time)
and producing a structured `MarketRegimeState` object. It leverages ADK callbacks
for robust logging, validation, and state management.
"""

import json
import logging
from typing import Dict, Any

import google.adk as adk
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from pydantic import ValidationError

from trade_weaver.config import MODEL_FLASH
from .prompt import INSTRUCTION
from .schemas import MarketRegimeState
from .tools import market_analyst_tools

# --- ADK Callbacks for Robustness and Observability ---

from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool

def validate_and_log_tool_output(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> None:
    """
    ADK `after_tool_callback` to perform structured logging and basic validation.
    """
    tool_name = tool.name

    # Structured logging for better observability
    log_data = {
        "event": "after_tool_call",
        "tool_name": tool_name,
        "tool_args": args,
        "tool_response": tool_response,
        "session_id": tool_context.session.id,
    }
    logging.info(json.dumps(log_data))

    # Basic validation for critical data points
    if tool_name == "get_vix_data":
        if isinstance(tool_response, dict):
            vix_value = tool_response.get("vix_value", -1)
            if vix_value < 0:
                logging.warning(f"VIX value {vix_value} is unrealistic.")

    if tool_name == "get_adx_data":
        if isinstance(tool_response, dict):
            adx_value = tool_response.get("adx_value", -1)
            if adx_value < 0:
                logging.warning(f"ADX value {adx_value} is unrealistic.")


def parse_and_save_intermediate_state(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> None:
    """
    ADK `after_model_callback` to parse, validate, and save structured state.

    This is a critical data integrity step. It finds the JSON block in the LLM's
    text response, validates it against the `MarketRegimeState` Pydantic schema,
    and if successful, saves the structured data to the session state. This makes
    the validated data available to subsequent tools like `persist_market_regime`.
    """
    if not llm_response:
        logging.warning("after_model_callback called but no llm_response found.")
        return

    if not llm_response.content or not llm_response.content.parts:
        logging.warning("LlmResponse has no content or parts to parse.")
        return
    model_response_text = "".join(
        part.text for part in llm_response.content.parts if part.text
    )
    log_data = {
        "event": "after_model_call",
        "model_response": model_response_text,
        "session_id": callback_context._invocation_context.session.id,
    }

    try:
        # Extract the JSON block from the model's response
        json_str_start = model_response_text.find("```json\n{")
        if json_str_start == -1:
            json_str_start = model_response_text.find("{")
        else:
            json_str_start += len("```json\n")

        json_str_end = model_response_text.rfind("}") + 1
        if json_str_start == -1 or json_str_end == 0:
             raise json.JSONDecodeError("No JSON object found in the model response.", model_response_text, 0)

        json_str = model_response_text[json_str_start:json_str_end]

        json_data = json.loads(json_str)

        # Validate the extracted data using the Pydantic schema
        validated_data = MarketRegimeState(**json_data)

        # Save the validated, structured data to the session state
        callback_context.state.update(
            {"intermediate_market_regime": validated_data.dict()}
        )
        log_data["status"] = "success"
        log_data["validated_data"] = validated_data.dict()

    except (json.JSONDecodeError, ValidationError) as e:
        log_data["status"] = "error"
        log_data["error_message"] = str(e)
        logging.error(f"Failed to parse or validate market regime state: {e}")

    logging.info(json.dumps(log_data))


# --- Agent Definition ---

market_analyst_agent = LlmAgent(
    name="market_analyst",
    description="Analyzes and reports on the current market regime.",
    model=MODEL_FLASH,
    instruction=INSTRUCTION,
    tools=market_analyst_tools,
    after_model_callback=parse_and_save_intermediate_state,
)
