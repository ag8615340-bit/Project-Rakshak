from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# CORS ko allow karna zaroori hai taaki frontend baat kar sake
CORS(app)

# 🔐 Load Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/details")
def details():
    return render_template("detail.html")

@app.route("/chat", methods=["POST"])
def chat():
    # 1. Check if API Key exists
    if not GROQ_API_KEY:
        return jsonify({"error": "API Key missing on server side"}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
            
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
                        "Draft HIGHLY FORMAL legal complaints. Tone: Authoritative, Serious. "
                        "No AI disclaimers like 'As an AI...'."
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

        # Timeout badha diya hai (45s) kyunki Render Free Tier slow hota hai
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=45)

        if response.status_code == 200:
            result = response.json()
            bot_reply = result['choices'][0]['message']['content']
            return jsonify({"reply": bot_reply})
        else:
            # Agar Groq se error aaye toh wo dikhayega
            print(f"Groq Error: {response.text}")
            return jsonify({"error": f"Groq Error: {response.status_code}"}), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Please try again."}), 504
    except Exception as e:
        print(f"🔥 Server Crash: {str(e)}")
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500

# --- 🚀 RENDER DEPLOYMENT SETTINGS ---
if __name__ == "__main__":
    # Render ke liye port 10000 default aur host 0.0.0.0 mandatory hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)