
# utils/constants.py
"""Constants and configuration values for the Chatbot Personality Designer."""

from pathlib import Path

# Project root path
PROJECT_ROOT = Path(__file__).parent.parent


# LLM API configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "phi3:mini" #Added because this Ollama model works on CPU with < 16GB RAM
REQUEST_TIMEOUT = 30  # seconds


# Temperature and token ranges (scaled from personality values)
MIN_TEMPERATURE = 0.3
MAX_TEMPERATURE = 1.0
MIN_TOKENS = 50
MAX_TOKENS = 200
CONTEXT_WINDOW_SIZE = 8
# Default personality values
DEFAULT_PERSONALITY = {
    "creativity": 0.5,
    "professionalism": 0.5,
    "friendliness": 0.5,
    "sarcasm": 0.0,
    "verbosity": 0.5
}

# Preset file path - FIXED: Use absolute path relative to project root
# This need a look in case of errors
PRESETS_FILE_PATH = PROJECT_ROOT / "config" / "default_presets.json"
