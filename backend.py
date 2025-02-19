from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for security

# System prompt to guide the chatbot
SYSTEM_PROMPT = """
You are a financial assistant chatbot for a FinTech company.
You provide accurate information about loans, interest rates, credit bureaus, credit reports, and CIBIL.
Ensure responses are factual, concise, and helpful.
"""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("user_message")
        if not user_message:
            return jsonify({"error": "User message is required"}), 400
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    
    except openai.error.OpenAIError as oe:
        return jsonify({"error": "OpenAI API error: " + str(oe)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use environment variable for port, default to 8000
    app.run(host="0.0.0.0", port=port, debug=True)
