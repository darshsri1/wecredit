import streamlit as st
import requests
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# AIML API details
API_KEY = "6ed1008879fc4c8a8904e99dd1b29542"
BASE_URL = "https://api.aimlapi.com/v1/chat/completions"

# System prompt
SYSTEM_PROMPT = """
You are a financial assistant chatbot for a FinTech company.
You provide accurate information about loans, interest rates, credit bureaus, credit reports, and CIBIL.
Ensure responses are factual, concise, and helpful.
"""

# Streamlit UI setup
st.set_page_config(page_title="We Credit Assistant", layout="centered")

# Sidebar branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("💰 We Credit Assistant")
    st.markdown("A smart chatbot to answer your financial queries!")
    temperature = st.slider("🎨 AI Creativity Level", 0.0, 1.0, 0.7)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
    }
    .chat-container {
        max-width: 700px;
        margin: auto;
    }
    .user-message {
        background-color: #DCF8C6;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 80%;
        font-size: 16px;
        color: black;
    }
    .assistant-message {
        background-color: #E3E3E3;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 80%;
        font-size: 16px;
        color: black;
    }
    .message-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .message-container .user {
        align-self: flex-end;
    }
    .message-container .assistant {
        align-self: flex-start;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "assistant-message"
    align_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f'<div class="message-container {align_class}"><div class="{role_class}">{msg["content"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# User input
user_input = st.chat_input("💬 Ask about loans, interest rates, or credit scores...")

def get_ai_response(user_text):
    """Fetch AI response from the AIML API."""
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": temperature
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return "🚨 API Error: Unable to fetch response."

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="message-container user"><div class="user-message">{user_input}</div></div>', unsafe_allow_html=True)

    # AI response
    with st.spinner("🤖 Thinking..."):
        time.sleep(1)  # Simulating processing delay
        ai_response = get_ai_response(user_input)

    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.markdown(f'<div class="message-container assistant"><div class="assistant-message">{ai_response}</div></div>', unsafe_allow_html=True)

    # Refresh UI
    st.rerun()
