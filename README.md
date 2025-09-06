# Personality Chatbot Designer

A dynamic Streamlit application that enables endless conversation with a locally-hosted Large Language Model (LLM). Fine-tune the AI's personality in real-time using intuitive sliders controlling creativity, professionalism, friendliness, sarcasm, and verbosity. Powered by Ollama for a seamless and private AI experience.

![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Ollama](https://img.shields.io/badge/LLM-Ollama-6D3FFF?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python)

## ✨ Features

-   **Real-Time Personality Adjustment:** Five interactive sliders to control the AI's response style.
-   **Local & Private:** Built for Ollama, ensuring complete data privacy and no API costs.
-   **Personality Presets:** Instantly apply curated profiles like "Professional Assistant" or "Sarcastic Buddy".
-   **Robust & Resilient:** Graceful fallback to sophisticated mock responses with clear user warnings if the local LLM is unavailable.
-   **Unlimited Conversation:** No artificial demo limits—chat as long as you like.

## 📋 Table of Contents

-   [Personality Chatbot Designer](#personality-chatbot-designer)
  - [✨ Features](#-features)
  - [📋 Table of Contents](#-table-of-contents)
  - [🛠️ Installation \& Setup](#️-installation--setup)
  - [🚀 Usage](#-usage)
  - [📁 Project Structure](#-project-structure)
  - [🔌 Swapping the LLM Provider: A Comparative Guide](#-swapping-the-llm-provider-a-comparative-guide)
    - [**Overview of Required Changes for a Swap:**](#overview-of-required-changes-for-a-swap)
    - [**Option 1: Switching to OpenRouter (Remote API)**](#option-1-switching-to-openrouter-remote-api)
    - [**Option 2: Switching to Mistral API (Another Remote API)**](#option-2-switching-to-mistral-api-another-remote-api)
  - [🧪 Running Tests](#-running-tests)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)
  - [⁉️ Troubleshooting](#️-troubleshooting)

## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```
    git clone https://github.com/your-username/personality-chatbot-designer.git
    cd personality-chatbot-designer
    ```

2.  **Install Python dependencies:**
    ```
    pip install -r requirements.txt
    ```
    *Primary dependencies: `streamlit`, `requests`*

3.  **Install & Setup Ollama:**
    1.  Download and install [Ollama](https://ollama.ai/).
    2.  Pull the DeepSeek model:
        ```
        ollama pull deepseek-r1:8b
        ```
    3.  Ensure the Ollama service is running (it usually starts automatically).

## 🚀 Usage

1.  Launch the application:
    ```
    streamlit run app.py
    ```
2.  Open your browser to the provided local URL (typically `http://localhost:8501`).
3.  Select a personality preset or use the sliders to create a custom profile.
4.  Start chatting! The AI's responses will reflect your chosen personality traits.

## 📁 Project Structure

```
personality-chatbot-designer/
├── app.py                 # Main Streamlit application (UI & control flow)
├── requirements.txt       # Python dependencies
├── config/
│   └── default_presets.json  # Pre-defined personality profiles
├── utils/
│   ├── __init__.py
│   ├── constants.py       # Configuration: URLs, model names, parameters
│   ├── ollama.py          # Client for the Ollama API
│   ├── mock_responses.py  # Fallback response generator
│   └── presets.py         # Loader for personality presets
└── README.md
```

## 🔌 Swapping the LLM Provider: A Comparative Guide

The application is architecturally designed with a **pluggable LLM client system**. The key to swapping providers lies in understanding the API contract defined by the `get_llm_response(prompt, history, personality)` function and adapting a new client to fulfill it.

### **Overview of Required Changes for a Swap:**

| Component | Change Required | Purpose |
| :--- | :--- | :--- |
| `utils/constants.py` | Update URL and Model constants. | Points the application to the correct API endpoint and model. |
| `utils/[new_provider].py` | Create a new client module. | Contains all the logic for formatting requests and parsing responses for the new API. |
| `app.py` | Update a single import line. | Tells the main app to use the new client module. |

### **Option 1: Switching to OpenRouter (Remote API)**

OpenRouter provides a unified API to access many closed- and open-source models.

**Step-by-Step Changes:**

1.  **Update `utils/constants.py`:**
    ```python
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    OPENROUTER_MODEL = "mistralai/mixtral-8x7b-instruct" # Example
    ```
2.  **Create `utils/openrouter.py`:** Adapt the API call to use OpenRouter's payload and headers (which require an API key). Reuse helper functions from `ollama.py`.
3.  **Update the import in `app.py`:**
    ```python
    from utils.openrouter import get_llm_response
    ```

### **Option 2: Switching to Mistral API**

The process is nearly identical to OpenRouter.

**Step-by-Step Changes:**

1.  **Update `utils/constants.py`:**
    ```python
    MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
    MISTRAL_MODEL = "mistral-large-latest"
    ```
2.  **Create `utils/mistral.py`:** Implement the client using Mistral's specific endpoint and authentication.
3.  **Update the import in `app.py`:**
    ```python
    from utils.mistral import get_llm_response
    ```

**Key Learning Points:** Swapping providers teaches API authentication, payload structure differences, and response parsing variations.


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## ⁉️ Troubleshooting

*   **`Failed to connect to Ollama...`:** Ensure the Ollama service is running. Run `ollama serve` in a terminal.
*   **`Model 'deepseek-r1:8b' not found`:** You need to pull the model. Run `ollama pull deepseek-r1:8b`.
*   **Mock responses are always used:** Check your terminal for error logs. This typically means the app cannot connect to the Ollama service.
