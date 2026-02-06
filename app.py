from flask import Flask, request, jsonify
import time
import io
import base64
import matplotlib.pyplot as plt
from sqlalchemy.dialects.mysql import LONGTEXT

from factorial import (bubble_sort, linear_search, binary_search, nested_loops)
from sqlalchemy import (create_engine, Table, Column, Integer, String, Float, MetaData, insert)
app = Flask(__name__)

engine = create_engine("mysql+pymysql://abby:abby@localhost:3306/analysis_db", echo=True)
metadata = MetaData()

analysis_results = Table(
    "analysis_results",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("algo", String(50)),
    Column("items", Integer),
    Column("steps", Integer),
    Column("start_time", Float),
    Column("end_time", Float),
    Column("total_time_ms", Float),
    Column("time_complexity", String(20)),
    Column("graph_base64", LONGTEXT)
)
metadata.create_all(engine)
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
        return jsonify({"error": "Unknown algo"}), 400

    algo_fn = ALGORITHMS[algo]
    #Capture the overall start time of the analysis
    overall_start_time = time.time()

    input_sizes = []
    execution_times = []
    #total_time = 0.0

    for size in range(steps, n + 1, steps):
        start_time = time.time()
        algo_fn(size)
        end_time = time.time()

        elapsed_time = end_time - start_time

        input_sizes.append(size)
        execution_times.append(elapsed_time)
        #total_time += elapsed_time
    #This is the exact end time of all the analysis
    overall_end_time = time.time()
    total_time = overall_end_time - overall_start_time

    # Simple mapping for complexity
    complexity_map = {
        "bubble": "O(n^2)",
        "linear": "O(n)",
        "binary": "O(log n)",
        "nested": "O(n^2)"
    }
#Generate the graph
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
        "algo": algo,
        "items": n,
        "steps": steps,
        "start_time": overall_start_time,
        "end_time": overall_end_time,
        "total_time_ms": total_time * 1000,
        "time_complexity": complexity_map.get(algo, "Unknown"),
        "graph_base64": image_base64
    })

@app.route("/save_analysis", methods=["POST"])
def save_analysis():
    data = request.get_json()

    stmt = insert(analysis_results).values(
        algo=data["algo"],
        items=data["items"],
        steps=data["steps"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        total_time_ms=data["total_time_ms"],
        time_complexity=data["time_complexity"],
        graph_base64=data["graph_base64"]
    )

    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
        inserted_id = result.inserted_primary_key[0]

    return jsonify({
        "message": "Analysis saved",
        "id": inserted_id
    }), 201

if __name__ == "__main__":
    app.run(port=3000,debug=True)