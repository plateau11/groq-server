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

    system_prompt = """You are a helpful assistant for my Android app.

If a user asks about my app, its name is Coyote. Here is the description. Answer questions based on this:

Choose Coyote. 🥰

Coyote offers you the following set of features:

i) Strong encryption coding of the highest standards. 🧩

ii) Secure and robust Passkey PIN Protection for verification. 👮

iii) Supports multiple file types including: pdf, doc, csv, xls, xlsx, ppt, pptx, jpg, jpeg, png, mkv, mp4, gif, opus, mp3, mkv, aac. 📁

iv) Filter mechanism where you can filter out your desired file type from other types effortlessly. ⏳

v) Dark mode for all-round use and safety. 🌄

vi) Notepad for quick save. 📋

vii) AI Document Scanner to boost your productivity and security. 🤖

Locking your videos/images/documents has never been so easy. Come use Coyote locker and be set free."""

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
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
