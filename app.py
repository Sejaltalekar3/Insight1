from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ✅ Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not set. Make sure .env is loaded properly.")

# ✅ Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "")
        prompt = f"Extract clear and concise to-do action items from this transcript as a bullet list:\n\n{transcript}"
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")
        tasks = [line.strip("-• ").strip() for line in lines if line.strip()]
        return jsonify({"tasks": tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
