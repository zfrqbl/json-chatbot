# utils/mock_responses.py
"""Mock responses for fallback when the LLM API is unavailable."""

import random
from typing import Dict

# Mock responses for different personality configurations
# (The "limit_reached" list has been removed as it's no longer needed)
MOCK_RESPONSES = {
    "high_sarcasm": [
        "Oh, wow, another message. I'm absolutely thrilled to be helping you.",
        "Fascinating. You've used yet another of your precious messages on this.",
        "Let me guess - you want a helpful response? How original.",
        "I'd love to help, but I'm too busy contemplating the meaning of your request.",
        "Sure, I'll answer that. Not like I have anything better to do."
    ],
    "high_friendliness": [
        "I'd be absolutely delighted to help with that! 😊",
        "What a wonderful question! Let me think about how best to assist you.",
        "I'm so glad you asked! Here's what I can tell you about that:",
        "You've come to the right place! I'm happy to help with your question.",
        "That's a great question! Let me share what I know about this topic."
    ],
    "high_professionalism": [
        "I will address your inquiry with the utmost professionalism.",
        "Thank you for your question. Based on the available information, I can provide the following response:",
        "I have analyzed your query and prepared the following comprehensive response.",
        "After careful consideration of your question, I've formulated this response:",
        "I appreciate your question. Allow me to provide a detailed and professional answer."
    ],
    "high_creativity": [
        "Imagine if answers were clouds - I'd give you the fluffiest one! But since they're not, here's my creative take:",
        "If this response were a painting, it would be a masterpiece of helpful information! Here's what I've created:",
        "Let's approach this from a completely new angle! What if we considered that...",
        "I'm going to answer this in a way nobody has ever answered before! Here's my innovative perspective:",
        "Prepare for a response that will take you on a journey of imagination and insight!"
    ],
    "default": [
        "I understand your question. Here's what I can tell you about that.",
        "Thanks for your message. Let me help with that.",
        "I've processed your question and here's my response.",
        "That's an interesting question. Here's what I think about it.",
        "Let me address that for you. Here's the information you requested."
    ]
}


def get_dominant_trait(personality: Dict) -> str:
    """
    Determine the dominant personality trait.
    
    Args:
        personality: Dictionary of personality traits
        
    Returns:
        str: Name of the dominant trait
    """
    # Remove verbosity as it's not a personality trait for response selection
    traits = {k: v for k, v in personality.items() if k != "verbosity"}
    return max(traits.items(), key=lambda x: x[1])[0]


def get_mock_response(personality: Dict) -> str:
    """
    Get a mock response based on personality settings.
    
    Args:
        personality: Dictionary of personality traits
        
    Returns:
        str: Appropriate mock response
    """
    # Determine which response set to use based on strongest personality trait
    dominant_trait = get_dominant_trait(personality)
    
    if dominant_trait == "sarcasm" and personality["sarcasm"] > 0.6:
        return random.choice(MOCK_RESPONSES["high_sarcasm"])
    elif dominant_trait == "friendliness" and personality["friendliness"] > 0.6:
        return random.choice(MOCK_RESPONSES["high_friendliness"])
    elif dominant_trait == "professionalism" and personality["professionalism"] > 0.6:
        return random.choice(MOCK_RESPONSES["high_professionalism"])
    elif dominant_trait == "creativity" and personality["creativity"] > 0.6:
        return random.choice(MOCK_RESPONSES["high_creativity"])
    else:
        return random.choice(MOCK_RESPONSES["default"])
