# utils/presets.py
"""Utility functions for loading and managing personality presets."""
import json
import logging
from pathlib import Path
from typing import Dict, Any
from utils.constants import PRESETS_FILE_PATH, DEFAULT_PERSONALITY

# Configure logging
logger = logging.getLogger(__name__)


def load_presets() -> Dict[str, Any]:
    """
    Load personality presets from JSON file. Falls back to defaults if file not found.
    
    Returns:
        Dict: Dictionary of personality presets
    """
    try:
        # Ensure the config directory exists
        PRESETS_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        if not PRESETS_FILE_PATH.exists():
            logger.warning(f"Presets file not found at {PRESETS_FILE_PATH}, using defaults")
            default_presets = get_default_presets()
            save_presets(default_presets)  # Create the file for the user
            return default_presets
            
        with open(PRESETS_FILE_PATH, "r", encoding="utf-8") as f:
            presets = json.load(f)
            logger.info(f"Loaded {len(presets)} presets from {PRESETS_FILE_PATH}")
            return presets
            
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse presets file: {str(e)}. Using defaults.")
        return get_default_presets()
    except Exception as e:
        logger.error(f"Error loading presets: {str(e)}. Using defaults.")
        return get_default_presets()


def get_default_presets() -> Dict[str, Any]:
    """
    Get default personality presets.
    
    Returns:
        Dict: Dictionary of default personality presets
    """
    return {
        "Professional": {
            "creativity": 0.3,
            "professionalism": 0.9,
            "friendliness": 0.6,
            "sarcasm": 0.0,
            "verbosity": 0.7
        },
        "Friendly": {
            "creativity": 0.5,
            "professionalism": 0.4,
            "friendliness": 0.9,
            "sarcasm": 0.1,
            "verbosity": 0.8
        },
        "Creative": {
            "creativity": 0.9,
            "professionalism": 0.3,
            "friendliness": 0.7,
            "sarcasm": 0.3,
            "verbosity": 0.9
        },
        "Sarcastic": {
            "creativity": 0.7,
            "professionalism": 0.2,
            "friendliness": 0.4,
            "sarcasm": 0.9,
            "verbosity": 0.6
        }
    }


def save_presets(presets: Dict[str, Any]) -> None:
    """
    Save personality presets to JSON file.
    
    Args:
        presets: Dictionary of personality presets to save
        
    Raises:
        Exception: If file cannot be written
    """
    try:
        with open(PRESETS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(presets)} presets to {PRESETS_FILE_PATH}")
    except Exception as e:
        error_msg = f"Error saving presets: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)
