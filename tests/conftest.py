# File: /trade-weaver/tests/conftest.py

import pytest
import pytest_asyncio  # <-- Import the asyncio plugin's fixture decorator
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from trade_weaver.agent import root_agent as coordinator_agent_instance

@pytest.fixture(scope="module")
def root_agent():
    """Provides a single, reusable instance of the CoordinatorAgent for tests."""
    return coordinator_agent_instance

@pytest_asyncio.fixture  # <--- THIS IS THE FIX
async def adk_test_harness(root_agent):
    """
    Provides a ready-to-use ADK runner and session service for tests.
    This fixture is 'async' and will create a new session for each test function.
    """
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name="test_app", session_service=session_service)
    
    # Yield the runner and service to the test function
    yield runner, session_service
    
    # Cleanup code can go here if needed after the test runs