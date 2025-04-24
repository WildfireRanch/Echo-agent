from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load .env variables before using them
load_dotenv()

# ✅ Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Set up Flask
app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({
        "status": "Echo is online",
        "mode": "universal agent",
        "openai_key_loaded": bool(os.getenv("OPENAI_API_KEY"))
    })

@app.route("/ping")
def ping():
    return "pong"

@app.route("/ask")
def ask():
    prompt = request.args.get("prompt", default="What's the best way to start my day?")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are Echo, a helpful personal agent."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
