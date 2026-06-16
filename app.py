from flask import Flask, render_template, request, jsonify
import os
import re
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


    # 🎓 STUDY MODE (general explanation)
    if "study" in msg:
        prompt = "Explain this topic like a school teacher in simple Hindi + examples:\n" + user_msg

    # 📖 STORY MODE
    elif "story" in msg:
        prompt = "Write a creative and interesting story in simple Hindi:\n" + user_msg

    # ❓ DOUBT SOLVER MODE
    elif "doubt" in msg:
        prompt = "Solve this doubt step-by-step in simple Hindi:\n" + user_msg

    # 🧬 BIOLOGY MODE
    elif any(w in msg for w in ["biology", "cell", "dna", "heart", "blood", "human", "plant"]):
        prompt = "Explain Biology topic in simple Hindi + diagrams style explanation:\n" + user_msg

    # 📜 HISTORY MODE
    elif any(w in msg for w in ["history", "war", "independence", "freedom", "king", "mughal", "british"]):
        prompt = "Explain History in story style simple Hindi:\n" + user_msg

    # 🧠 DEFAULT MODE (SMART TEACHER)
    else:
        prompt = "You are a smart AI tutor. Explain in simple Hindi for students:\n" + user_msg


    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Indian student tutor AI."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
    return jsonify({"reply": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
