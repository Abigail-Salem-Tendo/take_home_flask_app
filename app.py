from flask import Flask, request, jsonify
import time
import io
import base64
import matplotlib.pyplot as plt
from factorial import (bubble_sort, linear_search, binary_search, nested_loops)
app = Flask(__name__)

ALGORITHMS = {
    "bubble": bubble_sort,
    "linear": linear_search,
    "binary": binary_search,
    "nested": nested_loops
}
@app.route("/")
def home():
    return "The flask app is running"
@app.route("/analyze")
def analyze():
    algo = request.args.get("algo")
    n = request.args.get("n", type=int)
    steps = request.args.get("steps", type=int)

    if algo not in ALGORITHMS:
        return jsonify({"error": "Unknown algorithm"}), 400

    algo_fn = ALGORITHMS[algo]

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

    plt.figure()
    plt.plot(input_sizes, execution_times, marker="o")
    plt.xlabel("Input size (n)")
    plt.ylabel("Execution time (s)")
    plt.title(f"Time Complexity Analysis: {algo}")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return jsonify({
        "algorithm": algo,
        "n": n,
        "steps": steps,
        "input_sizes": input_sizes,
        "execution_times": execution_times,
        "total_time": total_time,
        "graph_generated": image_base64
    })
if __name__ == "__main__":
    app.run(port=3000,debug=True)