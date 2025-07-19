from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    payload = {
        "model": "llama3-8b-8192",  # or any other Groq-supported model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "Groq API failed", "details": response.text}), 500

    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
