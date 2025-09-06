# utils/ollama.py
"""Ollama LLM API integration for local models."""

import time
import requests
import logging
from typing import Dict, List

import streamlit as st
from utils.constants import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    REQUEST_TIMEOUT,
    MIN_TEMPERATURE,
    MAX_TEMPERATURE,
    MIN_TOKENS,
    MAX_TOKENS,
    CONTEXT_WINDOW_SIZE,
)

# Configure logging
logger = logging.getLogger(__name__)

# Rate limiting for the UX
_MIN_API_CALL_INTERVAL = 2.0

def _rate_limit() -> bool:
    """
    Simple session-based rate limiting for a smooth user experience.
    Returns True if request should proceed, False if should wait.
    
    Returns:
        bool: True if okay to call the API, False if should wait.
    """
    if "last_api_call_time" not in st.session_state:
        st.session_state.last_api_call_time = 0

    current_time = time.time()
    time_since_last_call = current_time - st.session_state.last_api_call_time

    if time_since_last_call < _MIN_API_CALL_INTERVAL:
        wait_time = _MIN_API_CALL_INTERVAL - time_since_last_call
        logger.info(f"Rate limit hit, need to wait {wait_time:.1f}s")
        return False

    st.session_state.last_api_call_time = current_time
    return True

def _validate_personality(personality: Dict) -> None:
    """
    Validate personality values are within expected ranges.
    
    Args:
        personality: Dictionary of personality traits
        
    Raises:
        ValueError: If any personality value is out of range
    """
    for trait, value in personality.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Personality trait '{trait}' must be between 0.0 and 1.0, got {value}")

def create_system_prompt(personality: Dict) -> str:
    """
    Create a system prompt based on personality settings.
    (Reused logic from the original openrouter.py)
    
    Args:
        personality: Dictionary of personality traits
        
    Returns:
        str: Formatted system prompt for the LLM
    """
    _validate_personality(personality)
    
    traits = []
    
    # Map personality traits to descriptive text
    if personality["professionalism"] > 0.7:
        traits.append("highly professional and formal")
    elif personality["professionalism"] < 0.3:
        traits.append("casual and informal")
    
    if personality["friendliness"] > 0.7:
        traits.append("extremely friendly and warm")
    elif personality["friendliness"] < 0.3:
        traits.append("somewhat reserved and direct")
    
    if personality["sarcasm"] > 0.7:
        traits.append("quite sarcastic and witty")
    elif personality["sarcasm"] > 0.4:
        traits.append("slightly sarcastic")
    
    if personality["creativity"] > 0.7:
        traits.append("highly creative and imaginative")
    elif personality["creativity"] < 0.3:
        traits.append("factual and straightforward")
    
    # Default trait if none specified
    if not traits:
        traits.append("helpful and informative")
    
    traits_text = ", ".join(traits)
    
    return f"""You are a chatbot with a personality that is {traits_text}.
    IMPORTANT INSTRUCTIONS:
- Provide only your final response, DO NOT show your reasoning process
- DO NOT use phrases like "Let me think..." or "Here's my reasoning..."
- DO NOT include any text before or after your actual response
- Respond directly and concisely as your personality would.
Respond appropriately based on your configured personality traits."""

def get_llm_response(prompt: str, message_history: List[Dict], personality: Dict) -> str:
    """
    Get response from a local LLM via the Ollama API.
    Maintains the exact same interface as the original OpenRouter function.
    
    Args:
        prompt: User's message prompt
        message_history: List of previous messages
        personality: Dictionary of personality traits
        
    Returns:
        str: LLM response content
        
    Raises:
        Exception: If API request fails or returns invalid response
    """
    # Check app-level rate limit first (for UX, not API)
    if not _rate_limit():
        raise Exception("rate_limit_exceeded")

    _validate_personality(personality)
    
    # Reuse the system prompt creation logic
    system_prompt_content = create_system_prompt(personality)
    
    # Prepare the messages list for the Ollama API.
    # Ollama uses a single 'messages' array and understands the 'system' role.
    messages = []
    
    # Add the system prompt as a message with role 'system'
    messages.append({"role": "system", "content": system_prompt_content})
    
    # Add conversation history (last few messages for context)
    for msg in message_history[-CONTEXT_WINDOW_SIZE:]:
        # Ensure role is one of 'system', 'user', 'assistant'
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Add the current user prompt
    messages.append({"role": "user", "content": prompt})
    
    # Calculate parameters based on personality (logic reused)
    temperature = MIN_TEMPERATURE + personality["creativity"] * (MAX_TEMPERATURE - MIN_TEMPERATURE)
    max_tokens = int(MIN_TOKENS + personality["verbosity"] * (MAX_TOKENS - MIN_TOKENS))
    
    # Construct the payload for the Ollama API.
    # The structure is different from OpenRouter.
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "options": { # Ollama-specific location for parameters
            "temperature": temperature,
            "num_predict": max_tokens, # Ollama's equivalent of max_tokens
        },
        "stream": False # We want a single, complete response
    }
    
    try:
        logger.info(f"Sending request to Ollama API with {len(messages)} messages")
        
        # Make the API request. No headers are needed for a local Ollama instance.
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # Raises an exception for HTTP errors (4xx, 5xx)
        
        # Parse the response
        result = response.json()
        
        # Ollama's response structure is different from OpenRouter.
        if "message" not in result:
            error_msg = "Invalid response format: 'message' field not found"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # Extract the final assistant message content
        return result["message"]["content"]
        
    except requests.exceptions.ConnectionError:
        error_msg = f"Failed to connect to Ollama. Is it running on {OLLAMA_URL}?"
        logger.error(error_msg)
        raise Exception(error_msg)
    except requests.exceptions.RequestException as e:
        error_msg = f"Ollama API request failed: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)
    except (KeyError, IndexError) as e:
        error_msg = f"Invalid response format from Ollama: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)
