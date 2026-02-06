from datetime import datetime
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
import matplotlib.pyplot as plt
from factorial import bubble_sort, linear_search, binary_search, nested_loops

app = Flask(__name__)

#Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://abby:abby@localhost:3306/analysis_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
test_db = SQLAlchemy(app)

#Map the Algorithms
ALGORITHMS = {
    "bubble_sort": bubble_sort,
    "linear_search": linear_search,
    "binary_search": binary_search,
    "nested_loops": nested_loops
}

time_complexities = {
    "bubble_sort": "O(n^2)",
    "linear_search": "O(n)",
    "binary_search": "O(log n)",
    "nested_loops": "O(n^2)"
}

#defining the model table
class AnalysisResult(test_db.Model):
    __tablename__ = "analysis_results"
    
    id = test_db.Column(test_db.Integer, primary_key=True)
    algo = test_db.Column(test_db.String(50), nullable=False)
    items = test_db.Column(test_db.Integer, nullable=False)
    steps = test_db.Column(test_db.Integer, nullable=False)
    start_time = test_db.Column(test_db.Float, nullable=False)
    end_time = test_db.Column(test_db.Float, nullable=False)
    total_time = test_db.Column(test_db.Float, nullable=False)
    time_complexity = test_db.Column(test_db.String(20), nullable=False)
    graph_image_path = test_db.Column(test_db.Text, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "algo": self.algo,
            "items": self.items,
            "steps": self.steps,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time": self.total_time,
            "time_complexity": self.time_complexity,
            "graph_image_path": self.graph_image_path,
        }
    
#Create the table
with app.app_context():
    test_db.create_all()

#Ensure graphs folder exists
graph_folder = "graphs"
os.makedirs(graph_folder, exist_ok=True)

#Define the routes
@app.route("/")
def home():
    return "The flask app is running"

@app.route("/analyze", methods=["GET"])
def analyze():
    algo = request.args.get("algo")
    items = request.args.get("items", type=int)
    steps = request.args.get("steps", type=int)
    
    if algo not in ALGORITHMS:
        return jsonify({"error": "Unknown algo"}), 400

    algo_fn = ALGORITHMS[algo]
    # Capture the overall start time of the analysis
    overall_start_time = time.time()

    input_sizes = []
    execution_times = []

    for size in range(steps, items + 1, steps):
        start_time = time.time()
        algo_fn(size)
        end_time = time.time()
        elapsed_time = end_time - start_time
        input_sizes.append(size)
        execution_times.append(elapsed_time)
    # This is the exact end time of all the analysis
    overall_end_time = time.time()
    total_time = overall_end_time - overall_start_time

    # # Simple mapping for complexity
    # complexity_map = {
    #     "bubble": "O(n^2)",
    #     "linear": "O(n)",
    #     "binary": "O(log n)",
    #     "nested": "O(n^2)"
    # }
    # Generate the graph
    plt.figure()
    plt.plot(input_sizes, execution_times, marker="o")
    plt.xlabel("Input size (n)")
    plt.ylabel("Execution time (s)")
    plt.title(f"Time Complexity Analysis: {algo}")

    #create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{algo}_{steps}_{timestamp}.png"
    graph_path = os.path.join(graph_folder, filename)

    #save grapgh to file
    plt.savefig(graph_path, format="png")
    plt.close()

    return jsonify({
        "algo": algo,
        "items": items,
        "steps": steps,
        "start_time": overall_start_time,
        "end_time": overall_end_time,
        "total_time_ms": total_time * 1000,
        "time_complexity": time_complexities.get(algo, "Unknown"),
        "graph_image_path": graph_path
    })

@app.route("/save_analysis", methods=["POST"])
def save_analysis():
    data = request.get_json()

    required_fields = [
        "algo",
        "items",
        "steps",
        "start_time",
        "end_time",
        "total_time_ms",
        "time_complexity",
        "graph_image_path"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": "Missing required field"}), 400

    new_result = AnalysisResult(
        algo=data["algo"],
        items=data["items"],
        steps=data["steps"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        total_time=data["total_time_ms"],
        time_complexity=data["time_complexity"],
        graph_image_path=data["graph_image_path"]
    )

    test_db.session.add(new_result)
    test_db.session.commit()

    return jsonify({
        "message": "Analysis saved!",
        "id": new_result.id
    }), 201

@app.route("/retrieve_analysis", methods=["GET"])
def retrieve_analysis():
    analysis_id = request.args.get("id", type=int)

    if analysis_id is None:
        return jsonify({"error": "Missing required parameter"}), 400

    result = AnalysisResult.query.get(analysis_id)

    if result is None:
        return jsonify({"error": "Analysis not found"}), 404

    return jsonify(result.to_dict())

if __name__ == "__main__":
    app.run(port=5000,debug=True)