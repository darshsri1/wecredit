import streamlit as st
import requests
import time

# Flask API URL
API_URL = "http://127.0.0.1:8080/chat"

# Streamlit UI setup
st.set_page_config(page_title="We Credit Assistant", layout="centered")

# Sidebar branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("💰 We Credit Assistant")
    st.markdown("A smart chatbot to answer your financial queries!")

# Custom CSS for chat bubble styling
st.markdown("""
    <style>
    .user-message {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 70%;
    }
    .assistant-message {
        background-color: #E3E3E3;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 70%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    st.markdown(f'<div class="{role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# User input field
user_input = st.text_input("💬 Ask about loans, interest rates, or credit scores:")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)

    # Show loading indicator
    with st.spinner("Thinking..."):
        time.sleep(1)  # Simulating processing delay
        response = requests.post(API_URL, json={"user_message": user_input})

    # Process response
    if response.status_code == 200:
        reply = response.json().get("response", "No response received.")
    else:
        reply = "⚠️ Error connecting to chatbot API."

    # Display chatbot response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(f'<div class="assistant-message">{reply}</div>', unsafe_allow_html=True)
