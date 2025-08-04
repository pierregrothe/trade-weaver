# File: tests/conftest.py

import pytest
from dotenv import load_dotenv
import os

def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing test collection and execution.

    This hook is used to load environment variables from the .env file
    at the project root, making them available to all tests.
    """
    print("\n--- Loading environment variables for pytest session ---")
    
    # Construct the path to the .env file at the project root
    # This assumes your 'tests' directory is at the project root.
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(project_root, '.env')

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        print("✅ .env file loaded successfully.")
        # Optional: check if the key is loaded
        if not os.getenv("GOOGLE_API_KEY"):
            print("⚠️ WARNING: GOOGLE_API_KEY not found in .env file.")
    else:
        print(f"⚠️ WARNING: .env file not found at {dotenv_path}. Tests requiring API keys may fail.")