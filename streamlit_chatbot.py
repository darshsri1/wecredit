import streamlit as st
import requests

# Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000/chat"  # Update this if deploying online

st.title("💰 We Credit Assistant Chatbot")
st.caption("📢 Ask financial queries related to loans, interest rates, and credit reports.")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Chatbot Settings")
    temperature = st.slider("Response Creativity (Temperature)", 0.0, 1.0, 0.7)

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# User input
user_message = st.chat_input("Ask your financial question...")

def get_chatbot_response(user_input):
    """Sends user input to Flask backend and retrieves chatbot response."""
    try:
        response = requests.post(FLASK_API_URL, json={"user_message": user_input})
        if response.status_code == 200:
            return response.json().get("response", "No response received.")
        else:
            return f"⚠️ Error {response.status_code}: {response.json().get('error', 'Unknown error')}"
    except requests.exceptions.RequestException as e:
        return f"🚨 API Error: {e}"

if user_message:
    # Display user message
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    # Get AI response
    with st.spinner("🤖 Thinking..."):
        ai_response = get_chatbot_response(user_message)

    # Display AI response
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    st.rerun()
