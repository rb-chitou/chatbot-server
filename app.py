from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"]
    api_key = os.environ.get("MISTRAL_API_KEY")

    if not api_key:
        return jsonify({"error": "MISTRAL_API_KEY not configured"}), 500

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Mistral API error", "details": response.text}), 500

    result = response.json()
    reply = result["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
