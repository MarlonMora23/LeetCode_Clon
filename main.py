"""
Web app for testing exercises.

This module contains the main web app for testing exercises. It uses Flask as the web server and
defines routes for the home page, submitting code, and displaying exercises.

The home page displays a link for each exercise. When a user clicks on a link, the user is taken
to the page for that exercise. The page displays the problem statement, the user's code, and a
submit button. When the user clicks the submit button, the app runs the user's code and displays
the result of the test.

The app also uses a problem solver module to run the user's code and check if the code is correct.
"""
import os
from flask import Flask, session, request, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from problem_solver.i_problem import IProblem
from problem_solver.problems.problem_1 import Problem1
from problem_solver.problems.problem_2 import Problem2
from problem_solver.problems.problem_3 import Problem3
from problem_solver.user_submission import UserSubmission
from problem_solver.handle_user_submission import test_problem


app: Flask = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'databases/users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}'
app.secret_key = os.environ.get("SECRET_KEY", "clave")
db: SQLAlchemy = SQLAlchemy(app)

class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(150), unique=True, nullable=False)
    email: str = db.Column(db.String(150), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(200), nullable=False)
    progress: dict = db.Column(db.PickleType, default={})  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
def get_problems() -> dict:
    """
    Returns a dictionary of IProblem instances, each representing one problem.

    The dictionary keys are the problem IDs and the values are instances of the
    corresponding IProblem class.

    Returns:
        dict: A dictionary of IProblem instances.
    """
    return {
        1: Problem1(),
        2: Problem2(),
        3: Problem3()
    }

def get_problem(problem_id: int) -> IProblem:
    """
    Returns an IProblem instance corresponding to the given problem ID.

    Args:
        problem_id (int): The ID of the problem to retrieve.

    Returns:
        IProblem: An instance of the IProblem class corresponding to the given problem ID.
    """
    problems_dict: dict = get_problems()

    return problems_dict[problem_id]

def get_number_of_problems() -> int:
    """
    Returns the number of problems in the system.

    Returns:
        int: The number of problems in the system.
    """
    return len(get_problems())

def get_problems_ids() -> list:
    """
    Returns a list of problem IDs as strings.

    Returns:
        list: A list of problem IDs as strings.
    """
    return list(str(key) for key in get_problems().keys())

@app.route('/login', methods=['POST'])
def login():
    data: dict = request.get_json()
    user: User = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful", "progress": user.progress}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/submit", methods=["POST"])
def submit_code() -> tuple:
    """
    Handles a POST request to /submit, which should contain a JSON payload
    with the following structure:

    {
        "problem_id": int,
        "code": str,
        "language": str
    }

    Returns a JSON object with the following keys:

    {
        "result": str,  # Success/Failure
        "feedback": str,  # Feedback for the user
        "expected_output": list,  # Expected output
        "tested_output": list  # User's output
    }

    If the request is invalid (e.g. missing fields), returns a JSON object
    with a single key "error" set to "Invalid request", and a status code of 400.

    If the language is unsupported, returns a JSON object with a single key
    "error" set to "Unsupported language", and a status code of 400.
    """
    data: dict = request.json

    if "problem_object" not in session:
        return jsonify({"error": "Invalid session"}), 400

    if "problem_id" not in data or "code" not in data or "language" not in data:
        return jsonify({"error": "Invalid request"}), 400

    problem_object: int = session["problem_object"]
    problem = globals()[problem_object]()

    submission = UserSubmission(
        problem_id=data["problem_id"], code=data["code"], language=data["language"]
    )

    if data["problem_id"] in get_problems_ids():
        return test_problem(problem, submission)

    return jsonify({"error": "Problem not found or unsupported language."}), 400


@app.route("/exercise/<int:exercise_id>")
def exercise(exercise_id):
    """
    Shows the exercise template for the given exercise_id.

    Args:
        exercise_id: The id of the exercise to be displayed.

    Returns:
        A rendered template with the exercise description, 
        or a 404 error if the exercise_id is not valid.
    """
    problem = get_problem(exercise_id)

    if problem:
        session["problem_object"] = f"Problem{exercise_id}"

        return render_template(f"exercise_{exercise_id}.html", problem=problem)

    return "Ejercicio no encontrado", 404


@app.route("/")
def index():
    """
    Handles a GET request to /.

    Returns a rendered HTML template for Exercise 1.
    """
    # Get the list of problems
    problems: list = [get_problem(i) for i in range(1, get_number_of_problems() + 1)]

    return render_template("landing.html", problems=problems)


def main():
    """
    Runs the Flask app on host 0.0.0.0 and port 8080.

    This function is the main entry point for the application.
    """
    # Create the database if it doesn't exist
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()
