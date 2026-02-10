# Algorithm Time Complexity Analyzer (Flask + MySQL + Base64 Graph)

This project is a Flask-based REST API that analyzes the runtime performance of common algorithms (Bubble Sort, Linear Search, Binary Search, and Nested Loops). It measures execution time across increasing input sizes, generates a runtime graph using Matplotlib, converts the graph into a Base64 string, and can store analysis results in a MySQL database using SQLAlchemy.

---

## Features

- Flask API with simple endpoints
- Supports 4 algorithms:
  - Bubble Sort
  - Linear Search
  - Binary Search
  - Nested Loops
- Measures execution time for increasing input sizes
- Generates a Matplotlib graph (execution time vs input size)
- Encodes the graph as Base64 and returns it in JSON
- Stores results into MySQL using SQLAlchemy
- Automatically creates the database table if it does not exist

---

## Project Structure

```txt
complexity_visualizer/
│
├── app.py                # Flask API (main application)
├── factorial.py          # Algorithm implementations
├── README.md             # Project documentation
└── .venv/                # Virtual environment (not committed to GitHub)
```

### 1. Prerequisites
* Python 3.8+
* MySQL Server
* Access to a MySQL user with `CREATE` privileges

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/Abigail-Salem-Tendo/take_home_flask_app.git
cd complexity_visualizer

# Create and activate virtual environment
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate  
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install flask flask-sqlalchemy mysql-connector-python matplotlib
```

### 3. Database Configuration
Ensure your MySQL server is running. You can set up the database by running:
```mysql
CREATE DATABASE analysis_db;
```

## Usage
Start the server
```
python3 app.py
```
The server will start on `http://localhost:5000`
