# File: src/trade_weaver/config.py

import os
from dotenv import load_dotenv

# Find the project root by going up from the current file's directory
# This makes the script work regardless of where it's run from.
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
DOTENV_PATH = os.path.join(PROJECT_ROOT, '.env')

# Load the .env file from the project root
load_dotenv(dotenv_path=DOTENV_PATH)

# --- AI Model Configuration ---
# Load the model names from environment variables, providing a default fallback.
LITE_MODEL = os.getenv("LITE_MODEL", "gemini-2.5-flash-lite")
FLASH_MODEL = os.getenv("FLASH_MODEL", "gemini-2.5-flash")
PRO_MODEL = os.getenv("PRO_MODEL", "gemini-2.5-pro")

# --- API Key Configuration ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# You can add other configurations here as the project grows.
print("✅ Configuration loaded.")
if not GOOGLE_API_KEY:
    print("⚠️ WARNING: GOOGLE_API_KEY is not set in the .env file.")