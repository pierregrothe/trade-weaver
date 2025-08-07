# File: /trade-weaver/trade_weaver/config.py
"""
Centralized configuration management for the Trade Weaver application.

This module loads environment variables from a .env file located at the project root,
validates critical settings, and provides typed, ready-to-use configuration
variables for the rest of the application.

It handles environment-specific settings (e.g., switching between live and paper
trading brokers) based on the APP_ENV variable.
"""

import os
from dotenv import load_dotenv
import logging

# --- 1. Path and Environment Loading ---
# Establishes the project root to reliably locate the .env file.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(PROJECT_ROOT, '.env')

if not os.path.exists(DOTENV_PATH):
    logging.warning(
        f".env file not found at {DOTENV_PATH}. "
        "Application may fail if required environment variables are not set."
    )
else:
    load_dotenv(dotenv_path=DOTENV_PATH)

# --- 2. Core Environment Settings ---
# Determines the operational mode of the application.
# Valid values: "development", "staging", "production"
APP_ENV = os.getenv("APP_ENV", "development").lower()


# --- 3. AI Platform & Model Configuration ---
MODEL_LITE="gemini-2.5-flash-lite"
MODEL_FLASH="gemini-2.5-flash"
MODEL_PRO="gemini-2.5-pro"


# Google AI platform selection
USE_VERTEX_AI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GCP_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT") # Renamed for consistency with .env
GCP_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# --- 4. Broker Configuration (Environment-Aware) ---
# This block dynamically selects broker credentials based on the APP_ENV.
if APP_ENV == "production":
    # Use LIVE trading credentials for production environment
    BROKER_HOST = os.getenv("BROKER_HOST", "127.0.0.1")
    BROKER_PORT = int(os.getenv("BROKER_PORT", "4001"))
    BROKER_ACCOUNT_ID = os.getenv("BROKER_ACCOUNT_ID")
else:
    # Default to PAPER trading credentials for development and staging
    BROKER_HOST = os.getenv("BROKER_PAPER_HOST", "127.0.0.1")
    BROKER_PORT = int(os.getenv("BROKER_PAPER_PORT", "4002"))
    BROKER_ACCOUNT_ID = os.getenv("BROKER_PAPER_ACCOUNT_ID")


# --- 5. Third-Party API Keys ---
EODHD_API_KEY = os.getenv("EODHD_API_KEY")
GOOGLE_CUSTOM_SEARCH_ENGINE_ID = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")


# --- 6. Operational Tuning Settings (Environment-Aware) ---
# Set a smart default for LOG_LEVEL based on the environment,
# but allow it to be overridden by an explicit setting in the .env file.
explicit_log_level = os.getenv("LOG_LEVEL")
if explicit_log_level:
    LOG_LEVEL = explicit_log_level.upper()
else:
    # Set smart defaults if not explicitly configured
    if APP_ENV == "production":
        LOG_LEVEL = "WARNING"
    elif APP_ENV == "staging":
        LOG_LEVEL = "INFO"
    else: # "development"
        LOG_LEVEL = "DEBUG"

API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "30"))
API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))


# --- 7. Startup Validation ---
# Fail-fast validation to ensure critical configurations are present.
def validate_configuration():
    """Checks for essential configs and raises ValueError if any are missing."""
    if not USE_VERTEX_AI and not GOOGLE_API_KEY:
        raise ValueError(
            "FATAL: GOOGLE_GENAI_USE_VERTEXAI is FALSE but GOOGLE_API_KEY is not set. "
            "Please provide your Google AI Studio API key in the .env file."
        )
    if USE_VERTEX_AI and not GCP_PROJECT_ID:
        raise ValueError(
            "FATAL: GOOGLE_GENAI_USE_VERTEXAI is TRUE but GOOGLE_CLOUD_PROJECT is not set. "
            "Please provide your GCP Project ID in the .env file."
        )
    if not BROKER_ACCOUNT_ID:
        env_var = "BROKER_ACCOUNT_ID" if APP_ENV == "production" else "BROKER_PAPER_ACCOUNT_ID"
        raise ValueError(
            f"FATAL: Broker account ID is not set for the '{APP_ENV}' environment. "
            f"Please set {env_var} in your .env file."
        )
    if not EODHD_API_KEY:
        logging.warning(
            "WARN: EODHD_API_KEY is not set. Financial data tools will fail."
        )
    logging.info(f"Configuration loaded successfully for '{APP_ENV}' environment.")
    logging.info(f"Connecting to broker at {BROKER_HOST}:{BROKER_PORT} for account {BROKER_ACCOUNT_ID}")

# Run validation when the module is imported
validate_configuration()