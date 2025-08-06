import logging
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai.types import Content

logger = logging.getLogger(__name__)


def log_agent_entry(callback_context: CallbackContext) -> Optional[Content]:
    """Logs the entry of an agent run, including session state for debugging."""
    logger.info(
        "ENTERING AGENT: %s (Invocation: %s)",
        callback_context.agent_name,
        callback_context.invocation_id,
    )
    # Log the state for debugging purposes, if it exists.
    if callback_context.state:
        logger.debug("Agent %s initial state: %s", callback_context.agent_name, callback_context.state.to_dict())
    return None


def log_agent_exit(callback_context: CallbackContext) -> Optional[Content]:
    """Logs the exit of an agent run."""
    logger.info(
        "EXITING AGENT: %s (Invocation: %s)",
        callback_context.agent_name,
        callback_context.invocation_id,
    )
    return None