import streamlit as st
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# AIML API details
API_KEY = "6ed1008879fc4c8a8904e99dd1b29542"
BASE_URL = "https://api.aimlapi.com/v1/chat/completions"

SYSTEM_PROMPT = """
You are a financial assistant chatbot for a FinTech company.
You provide accurate information about loans, interest rates, credit bureaus, credit reports, and CIBIL.
Ensure responses are factual, concise, and helpful.
"""

# Streamlit UI
st.title("💰 We Credit Assistant Chatbot")
st.caption("📢 Ask financial queries related to loans, interest rates, and credit reports.")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Chatbot Settings")
    temperature = st.slider("Response Creativity (Temperature)", 0.0, 1.0, 0.7)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# User input
user_message = st.chat_input("Ask your financial question...")

def get_ai_response(user_input):
    """Sends user input to AIML API and returns the chatbot's response."""
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
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
        response_data = response.json()

        # Extract AI response
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
    
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return "🚨 API Error: Unable to fetch response."

if user_message:
    # Display user message
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    # Get AI response
    with st.spinner("🤖 Generating response..."):
        ai_response = get_ai_response(user_message)

    # Display AI response
    st.session_state.chat_history.append({"role": "ai", "content": ai_response})
    st.rerun()
