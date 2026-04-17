from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "ACEest Fitness & Gym"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/members")
def members():
    return "Members page"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)