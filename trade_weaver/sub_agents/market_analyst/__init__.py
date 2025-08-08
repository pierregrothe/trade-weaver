# File: /trade_weaver/sub_agents/market_analyst/__init__.py
"""
Makes the Market Analyst agent easily importable as a package.

This allows the root agent or other parts of the system to simply use:
`from trade_weaver.sub_agents.market_analyst import market_analyst_agent`
"""
from .agent import market_analyst_agent
