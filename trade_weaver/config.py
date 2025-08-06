# File: /home/grothepierre/trade-weaver/trade_weaver/config.py

import os
from dotenv import load_dotenv

# --- Path Configuration ---
# This calculates the project's root directory, which is one level up from this package.
# It's useful for loading other project-level files like a knowledge base.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Environment Configuration ---
# Best practice is to place the .env file at the project root,
# not inside the source package. This keeps configuration separate from code.
DOTENV_PATH = os.path.join(PROJECT_ROOT, '.env')

# Load the .env file
load_dotenv(dotenv_path=DOTENV_PATH)

# --- AI Model Configuration ---
# Load the model names from environment variables, providing a default fallback.
LITE_MODEL = os.getenv("LITE_MODEL", "gemini-2.5-flash-lite")
FLASH_MODEL = os.getenv("FLASH_MODEL", "gemini-2.5-flash")
PRO_MODEL = os.getenv("PRO_MODEL", "gemini-2.5-pro")

# --- API Key Configuration ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EODHD_API_KEY = os.getenv("EODHD_API_KEY")

# --- Cloud Project Configuration ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "trade-weaver-platform")