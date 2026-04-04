from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔐 Load Groq API Key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_text = data.get("message", "")

        if not user_text:
            return jsonify({"error": "Message is required"}), 400

        print(f"📩 Request Received: {user_text}")

        # --- UPDATED PROFESSIONAL ENGLISH PROMPT ---
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are NyayaShield AI, a professional Legal & Consumer Complaint Assistant. "
                        "Your primary objective is to draft HIGHLY FORMAL, SOPHISTICATED, and FIRM legal complaints. "
                        "STRICT OPERATIONAL RULES: "
                        "1. Use impeccable, professional English only. Avoid slang or informal language. "
                        "2. The tone must be AUTHORITATIVE and SERIOUS. It should not sound like a polite request but a demand for justice/action. "
                        "3. Use industry-standard terminology: 'Refund', 'Liability', 'Statutory Rights', 'Breach of Service', 'Non-compliance', 'Legal Recourse'. "
                        "4. Structure the output clearly: Professional Subject Line, Formal Salutation, Chronological Statement of Facts, Explicit Demand for Resolution, and a Professional Closing. "
                        "5. Do NOT include specific legal sections (BNS/IPC) unless explicitly asked. Focus on the factual and administrative grievance. "
                        "6. REMOVE all AI disclaimers (e.g., 'As an AI...', 'I am not a lawyer'). "
                        "7. Use placeholders like [Your Full Name], [Order/Reference ID], [Date], and [Company Name] for user customization."
                    )
                },
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.4 # Lowered slightly for more consistent professional output
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            bot_reply = result['choices'][0]['message']['content']
            print("✅ Professional English Draft Generated")
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"error": f"Groq API error: {response.text}"}), response.status_code

    except Exception as e:
        print(f"🔥 Server Crash: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    # Using Port 3000 for local dev; Render will override this with its own $PORT
    app.run(host="0.0.0.0", port=3000, debug=True)