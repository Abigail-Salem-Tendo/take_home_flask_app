from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return "The flask app is running"
@app.route("/analyze")
def analyze():
    algo = request.args.get("algo")
    n = request.args.get("n", type=int)
    steps = request.args.get("steps", type=int)

    return jsonify({
        "algorithm": algo,
        "n": n,
        "steps": steps
    })
if __name__ == "__main__":
    app.run(port=3000,debug=True)