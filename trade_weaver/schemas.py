# File: /trade_weaver/schemas.py
"""
Defines the Pydantic data models for structured inputs and outputs.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any

class AgentTaskPayload(BaseModel):
    """
    Defines the structured JSON payload for an incoming machine-to-machine task.
    """
    target_agent: str = Field(
        description="The name of the specialist sub-agent to delegate the task to."
    )
    parameters: Dict[str, Any] = Field(
        description="A dictionary of parameters to be passed to the target agent's tools."
    )