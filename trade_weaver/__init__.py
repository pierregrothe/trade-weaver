# File: /trade_weaver/__init__.py
"""
Initializes the trade_weaver package and exposes the root_agent.
"""

# Import the agent instance from the agent.py file.
# This allows other parts of the application to import the root agent directly
# from the trade_weaver package, like so:
# from trade_weaver import root_agent
from .agent import root_agent