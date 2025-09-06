"""Chatbot Personality Designer - Main Streamlit application."""
import streamlit as st
import logging
from utils.ollama import get_llm_response
from utils.mock_responses import get_mock_response
from utils.presets import load_presets
from utils.constants import DEFAULT_PERSONALITY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Chatbot Personality Designer",
    page_icon="🤖",
    layout="wide"
)

def initialize_session_state() -> None:
    """Initialize all session state variables with default values."""
    defaults = {
        "messages": [],
        "personality": DEFAULT_PERSONALITY.copy(),
        "api_available": True,
        "current_preset": "Custom",  # Track the currently selected preset
        "show_system_prompt": False  # For the educational view we'll add later
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_conversation() -> None:
    """Reset the conversation history and message count, keeping the personality."""
    st.session_state.messages = []
    st.session_state.api_available = True
    st.success("Conversation reset! Personality settings retained.")

def apply_preset(preset_name: str) -> None:
    """
    Apply a personality preset to the current configuration.
    
    Args:
        preset_name: Name of the preset to apply
    """
    if preset_name == "Custom":
        return
        
    presets = load_presets()
    if preset_name in presets:
        st.session_state.personality = presets[preset_name].copy()
        st.session_state.current_preset = preset_name
        st.success(f"Applied '{preset_name}' preset!")
        logger.info(f"Applied preset: {preset_name}")


def render_personality_sidebar() -> None:
    """Render the sidebar with personality configuration controls."""
    with st.sidebar:
        st.header("🎛️ Personality Configuration")
        
        # Preset selection
        presets = load_presets()
        preset_names = list(presets.keys()) + ["Custom"]
        
        selected_preset = st.selectbox(
            "Choose a preset:",
            options=preset_names,
            index=preset_names.index(st.session_state.current_preset),
            help="Select a predefined personality profile or choose Custom to adjust manually",
            key="preset_selector"
        )
        
        if selected_preset != st.session_state.current_preset:
            apply_preset(selected_preset)
        
        # Personality sliders
        st.subheader("Adjust Personality Traits")
        
        st.session_state.personality["creativity"] = st.slider(
            "Creativity", 0.0, 1.0, st.session_state.personality["creativity"],
            help="How creative and imaginative the responses should be"
        )
        
        st.session_state.personality["professionalism"] = st.slider(
            "Professionalism", 0.0, 1.0, st.session_state.personality["professionalism"],
            help="How formal and professional the responses should be"
        )
        
        st.session_state.personality["friendliness"] = st.slider(
            "Friendliness", 0.0, 1.0, st.session_state.personality["friendliness"],
            help="How warm and friendly the responses should be"
        )
        
        st.session_state.personality["sarcasm"] = st.slider(
            "Sarcasm", 0.0, 1.0, st.session_state.personality["sarcasm"],
            help="How sarcastic and witty the responses should be"
        )
        
        st.session_state.personality["verbosity"] = st.slider(
            "Verbosity", 0.0, 1.0, st.session_state.personality["verbosity"],
            help="How detailed and lengthy the responses should be"
        )
        
        # Add a reset button
        st.divider()
        if st.button("🔄 Reset Conversation", use_container_width=True):
            reset_conversation()
        
        # ADD THE GOODBYE BUTTON HERE
        if st.button("👋 Goodbye", type="primary", use_container_width=True):
            st.success("Thank you for chatting! Goodbye.")
            st.stop() # This gracefully exits the app
        
        # Information section - UPDATE the demo info text
        st.info("""
        **Application Information:**
        - Adjust sliders to customize the chatbot's personality in real-time.
        - API calls use a local DeepSeek model via Ollama.
        - Mock responses are used if the local API is unavailable.
        """)

def render_chat_interface() -> None:
    """Render the main chat interface."""
    
    # PERSISTENT WARNING: Show a clear banner if API is unavailable
    if not st.session_state.api_available:
        st.warning(
            "⚠️ **Local LLM Unavailable**: You are currently seeing mock responses. "
            "Please ensure Ollama is running on your machine to use the full AI capabilities.",
            icon="⚠️"
        )
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # SINGLE chat input handling
    if prompt := st.chat_input("Type your message here...", key="chat_input"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if st.session_state.api_available:
                        response = get_llm_response(
                            prompt, 
                            st.session_state.messages, 
                            st.session_state.personality
                        )
                    else:
                        raise Exception("API marked as unavailable")
                        
                except Exception as e:
                    if "rate_limit_exceeded" in str(e):
                        # Handle rate limiting specifically
                        st.warning("⏳ Please wait a moment before sending another message. (Rate limit protection)")
                        response = "I'm processing messages too quickly! Please wait 2 seconds before sending another message."
                    else:
                        # Handle other API errors - ENHANCED USER FEEDBACK
                        error_msg = f"**Connection Failed**: Could not reach the local Ollama service. Using a mock response. Details: {str(e)}"
                        st.error(error_msg, icon="🚨") # More prominent error in the chat
                        logger.error(f"Ollama API Error: {str(e)}")
                        st.session_state.api_available = False # Set the global flag to fallback mode
                        response = get_mock_response(st.session_state.personality)
                
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

def main() -> None:
    """Main application function."""
    st.title("Chatbot Personality Designer 🤖")
    
    # Initialize session state
    initialize_session_state()
    
    # Create layout
    render_personality_sidebar()
    render_chat_interface()


if __name__ == "__main__":
    main()
