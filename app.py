from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔐 Load Groq API Key from Environment Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- ROUTES ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/details")
def details():
    return render_template("detail.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_text = data.get("message", "")

        if not user_text:
            return jsonify({"error": "Message is required"}), 400

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are NyayaShield AI, a professional Legal & Consumer Complaint Assistant. "
                        "Your primary objective is to draft HIGHLY FORMAL, SOPHISTICATED, and FIRM legal complaints. "
                        "Tone: Authoritative, Serious, Impeccable English. No AI disclaimers."
                    )
                },
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.4 
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            bot_reply = result['choices'][0]['message']['content']
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"error": f"Groq API error: {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

# --- 🚀 RENDER DEPLOYMENT SETTINGS ---
if __name__ == "__main__":
    # 1. Render automatically sets the PORT environment variable. 
    # Defaulting to 10000 which is Render's standard.
    port = int(os.environ.get("PORT", 10000))
    # 2. host="0.0.0.0" is MANDATORY for cloud deployment.
    app.run(host="0.0.0.0", port=port)