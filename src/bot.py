from flask import Flask, request, jsonify

app = Flask(__name__)

def optimize_prompt(prompt: str) -> str:
    # Basic optimization logic (placeholder)
    return "Optimized: " + prompt.strip()

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.json
    prompt = data.get("prompt", "")
    return jsonify({"optimized_prompt": optimize_prompt(prompt)})

if __name__ == "__main__":
    app.run(debug=True)
