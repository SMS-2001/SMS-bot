from flask import Flask, render_template, request, jsonify
import os
import re
from google import genai

app = Flask(__name__)

# 🔑 GEMINI API CLIENT
# यह अपने आप आपके सिस्टम या Render से "GEMINI_API_KEY" नाम का एनवायरनमेंट वेरिएबल उठा लेगा
client = genai.Client()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    if not user_msg:
        return jsonify({"reply": "No message received 😢"})

    msg = user_msg.lower()

    # 🧮 MATH MODE
    if re.fullmatch(r"[0-9\+\-\*\/\s\(\)]+", user_msg):
        try:
            result = eval(user_msg)
            return jsonify({"reply": f"🧮 Answer: {result}"})
        except:
            return jsonify({"reply": "Invalid math expression 😢"})

    # 🎓 STUDY MODE
    if "study" in msg:
        prompt = "Explain like a school teacher in simple Hindi:\n" + user_msg

    # 📖 STORY MODE
    elif "story" in msg:
        prompt = "Write a creative story in simple Hindi:\n" + user_msg

    # ❓ DOUBT MODE
    elif "doubt" in msg:
        prompt = "Solve step-by-step in simple Hindi:\n" + user_msg

    # 🧬 BIOLOGY MODE
    elif any(w in msg for w in ["biology", "cell", "dna", "heart", "blood", "plant", "human"]):
        prompt = "Explain Biology in simple Hindi with examples:\n" + user_msg

    # 📜 HISTORY MODE
    elif any(w in msg for w in ["history", "war", "independence", "freedom", "mughal", "british", "king"]):
        prompt = "Explain History in story style simple Hindi:\n" + user_msg

    # 🧠 DEFAULT MODE
    else:
        prompt = "You are a helpful Indian student tutor. Explain simply in Hindi:\n" + user_msg

    try:
        # 🤖 Gemini 2.5 Flash मॉडल का उपयोग (यह बहुत तेज़ और मुफ़्त/सस्ता है)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        reply = response.text

        if not reply:
            reply = "AI empty response 😢"

    except Exception as e:
        # 🔥 REAL ERROR SHOW (IMPORTANT)
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
