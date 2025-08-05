# app/market_analyst/agent.py
from google.adk.agents import LlmAgent
from app.market_analyst.tools import screen_exchanges_tool
from app.market_analyst.prompt import instruction
from app.config import GEMINI_MODEL

market_analyst = LlmAgent(
    name="market_analyst",
    model=GEMINI_MODEL,
    description="A specialized agent that screens stock exchanges to identify potential trading opportunities based on quantitative criteria.",
    instruction=instruction,
    tools=[screen_exchanges_tool]
)
