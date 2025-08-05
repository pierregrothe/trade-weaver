# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file in the project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- EODHD API Configuration ---
EODHD_API_KEY = os.getenv("EODHD_API_KEY")

# --- Model Configuration ---
GEMINI_MODEL = "gemini-1.5-flash-latest"

# --- Validation ---
if not EODHD_API_KEY:
    raise ValueError("EODHD_API_KEY environment variable not found. Please ensure it is set in your .env file.")
