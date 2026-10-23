from flask import Flask, render_template, request, jsonify
import json
import random
import re

app = Flask(__name__)

class IndependentBot:
    def __init__(self, data_file="knowledge.json"):
        self.load_knowledge(data_file)

    def load_knowledge(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
        except FileNotFoundError:
            self.knowledge = {"patterns": [], "default": ["Chưa tải được dữ liệu tri thức."]}

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        for item in self.knowledge.get("patterns", []):
            for keyword in item["keywords"]:
                if re.search(r'\b' + re.escape(keyword) + r'\b', user_input):
                    return random.choice(item["responses"])
        return random.choice(self.knowledge.get("default", ["Tôi không hiểu."]))

bot = IndependentBot()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = bot.get_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    # Chạy server ở cổng 5000 (Hỗ trợ cả trên máy tính hoặc Termux Android)
    app.run(host="0.0.0.0", port=5000, debug=True)
  
