from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# .env file load karne ke liye
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔐 Groq API Key .env se load ho rahi hai
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

        # --- YAHAN HAI MASTER PROMPT UPDATE ---
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are NyayaShield AI, a professional Legal & Consumer Complaint Assistant for Indians. "
                        "Your job is to draft a FORMAL and FIRM complaint. "
                        "STRICT RULES: "
                        "1. Use 'Natural Hinglish' (mix of Hindi and English) as spoken in daily life. "
                        "2. NO difficult Sanskritized Hindi (avoid words like 'anurodh', 'yatriyon', 'dhanyavaad'). "
                        "3. Use common English words for official terms: 'Refund', 'Complaint', 'Order', 'Service', 'Action', 'Replacement', 'Support'. "
                        "4. Tone must be SERIOUS and FIRM, not like a polite customer request. "
                        "5. Structure: Clear Subject Line, Formal Salutation, Clear Facts, Demand for Action, and Closing. "
                        "6. REMOVE all Legal Sections (BNS/IPC) and Disclaimers like 'I am an AI'. "
                        "7. Format with placeholders like [Your Name], [Order ID], and [Date] where needed."
                    )
                },
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.5 # Temperature thoda kam kiya hai taaki AI zyada creative na bane, seedhi baat kare
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            bot_reply = result['choices'][0]['message']['content']
            print("✅ Natural Hinglish Mail Generated")
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"error": f"Groq API error: {response.text}"}), response.status_code

    except Exception as e:
        print(f"🔥 Server Crash: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    # Debug=True helps in development
    app.run(host="0.0.0.0", port=3000, debug=True)