from flask import Flask, request, render_template, jsonify, redirect, url_for
from problem_solver.problems.problem_1 import Problem1
from problem_solver.problems.problem_2 import Problem2
from problem_solver.problems.problem_3 import Problem3
from problem_solver.handle_user_submission import test_problem
from problem_solver.user_submission import UserSubmission
from flask import session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "una_clave_secreta_por_defecto")


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

    if data["problem_id"] == "1":
        return test_problem(problem, submission)

    if data["problem_id"] == "2":
        return test_problem(problem, submission)

    if data["problem_id"] == "3":
        return test_problem(problem, submission)

    return jsonify({"error": "Problem not found or unsupported language."}), 400


@app.route("/exercise/<int:exercise_id>")
def exercise(exercise_id):
    """
    Shows the exercise template for the given exercise_id.

    Args:
        exercise_id: The id of the exercise to be displayed.

    Returns:
        A rendered template with the exercise description, or a 404 error if the exercise_id is not valid.
    """
    if exercise_id == 1:
        problem = Problem1()
        session["problem_object"] = "Problem" + str(problem.get_problem_id())

        return render_template("exercise_1.html", problem=problem)

    if exercise_id == 2:
        problem = Problem2()
        session["problem_object"] = "Problem" + str(problem.get_problem_id())

        return render_template("exercise_2.html", problem=problem)

    if exercise_id == 3:
        problem = Problem3()
        session["problem_object"] = "Problem" + str(problem.get_problem_id())

        return render_template("exercise_3.html", problem=problem)

    else:
        return "Ejercicio no encontrado", 404


@app.route("/")
def index():
    """
    Handles a GET request to /.

    Returns a rendered HTML template for Exercise 1.
    """
    # Redirect to Exercise 1 by default.
    return redirect(url_for("exercise", exercise_id=1))


def main():
    """
    Runs the Flask app on host 0.0.0.0 and port 8080.

    This function is the main entry point for the application.
    """
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()
