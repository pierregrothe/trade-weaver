# File: /trade_weaver/agent.py
"""
Defines the root Coordinator Agent using a custom, deterministic dispatcher.
This is a high-performance, non-LLM agent for M2M routing.
"""
import json
from typing import AsyncGenerator

# Correct, validated ADK import paths
from google.adk.agents import BaseAgent, InvocationContext
from google.adk.events import Event
from google.genai.types import Content, Part

# --- Sub-Agent Imports (Placeholders) ---
from .sub_agents.market_analyst import market_analyst_agent
# from .sub_agents.executor.agent import executor_agent


class CoordinatorAgent(BaseAgent):
    """
    A custom agent that deterministically dispatches tasks to sub-agents
    based on a JSON payload. It does not use an LLM for routing.
    """

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:

        # Helper function to create a properly structured error event
        def create_error_event(error_message: str) -> Event:
            error_payload = {
                "status": "error",
                "source_agent": self.name,
                "result": {"error_message": error_message},
            }
            return Event(
                author=self.name,
                content=Content(parts=[Part(text=json.dumps(error_payload))]),
            )

        # 1. Get the incoming JSON payload from the user's message
        if not (
            ctx.user_content
            and ctx.user_content.parts
            and ctx.user_content.parts[0].text
        ):
            yield create_error_event("No JSON payload provided.")
            return

        payload_str = ctx.user_content.parts[0].text
        try:
            payload = json.loads(payload_str)
            target_agent_name = payload.get("target_agent")
            parameters = payload.get("parameters", {})
        except json.JSONDecodeError:
            yield create_error_event("Invalid JSON payload.")
            return

        if not target_agent_name:
            yield create_error_event("'target_agent' key missing from JSON payload.")
            return

        # 2. Find the target sub-agent by name
        target_agent = self.find_sub_agent(target_agent_name)

        if not target_agent:
            yield create_error_event(f"Sub-agent '{target_agent_name}' not found.")
            return

        # 3. Update the session state with the parameters for the sub-agent
        for key, value in parameters.items():
            ctx.session.state[key] = value

        # 4. Directly invoke the sub-agent pipeline and stream its events back
        async for event in target_agent.run_async(ctx):
            yield event

        # 5. After the pipeline completes, capture the final result from the state
        final_result = ctx.session.state.get("validated_market_regime")

        if not final_result:
            yield create_error_event(
                "Pipeline completed, but 'validated_market_regime' not found in state."
            )
            return

        # 6. Construct and yield the final, consolidated M2M payload
        success_payload = {
            "status": "success",
            "source_agent": self.name,
            "result": final_result,
        }
        yield Event(
            author=self.name,
            content=Content(parts=[Part(text=json.dumps(success_payload))]),
        )


# --- Agent Instantiation ---
root_agent = CoordinatorAgent(
    name="trading_desk_coordinator",
    description="The main deterministic coordinator agent for M2M task routing.",
    # This custom agent has no model, prompt, or tools of its own.
    sub_agents=[
        market_analyst_agent,
        # executor_agent,
    ],
)
