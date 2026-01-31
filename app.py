from flask import Flask, request, jsonify
import time
import factorial
from factorial import (bubble_sort, linear_search, binary_search, nested_loops)
app = Flask(__name__)

@app.route("/")
def home():
    return "The flask app is running"
@app.route("/analyze")
def analyze():
    algo = request.args.get("algo")
    n = request.args.get("n", type=int)
    steps = request.args.get("steps", type=int)

    if algo not in factorial:
        return jsonify({"error": "Uknown algorithm"}), 400

    algo_fn = factorial[algo]

    input_sizes = []
    execution_times = []
    total_time = 0.0

    for size in range(steps, n + 1, steps):
        start_time = time.time()
        algo_fn(size)
        end_time = time.time()

        elapsed_time = end_time - start_time

        input_sizes.append(size)
        execution_times.append(elapsed_time)
        total_time += elapsed_time


    return jsonify({
        "algorithm": algo,
        "n": n,
        "steps": steps,
        "input_sizes": input_sizes,
        #"execution_times": execution_times,
        #"total_time": total_time
        "graph_generted": True
    })
if __name__ == "__main__":
    app.run(port=3000,debug=True)