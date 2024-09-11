from flask import Flask, render_template, request, jsonify
from problems.problem_1.problem_1 import test_problem_1, get_metadata
from problems.problem_2.problem_2 import test_problem_2
from problems.problem_3.problem_3 import test_problem_3

app = Flask(__name__)


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
        "expected_output": list[int],  # Expected output
        "tested_output": list[int]  # User's output
    }

    If the request is invalid (e.g. missing fields), returns a JSON object
    with a single key "error" set to "Invalid request", and a status code of 400.

    If the language is unsupported, returns a JSON object with a single key
    "error" set to "Unsupported language", and a status code of 400.
    """
    data: dict = request.json

    if "problem_id" not in data or "code" not in data or "language" not in data:
        return jsonify({"error": "Invalid request"}), 400

    if data["problem_id"] == "1":
        return test_problem_1(data)

    if data["problem_id"] == "2":
        return test_problem_2(data)

    if data["problem_id"] == "3":
        return test_problem_3(data)

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
    metadata = get_metadata()
    exercise_metadata = metadata.get(exercise_id)

    if exercise_id == 1:
        return render_template("exercise_1.html", metadata=exercise_metadata)
    elif exercise_id == 2:
        return render_template("exercise_2.html", metadata=exercise_metadata)
    elif exercise_id == 3:
        return render_template("exercise_3.html", metadata=exercise_metadata)
    else:
        return "Ejercicio no encontrado", 404


@app.route("/")
def index():
    """
    Handles a GET request to /.

    Returns a rendered HTML template for Exercise 1.
    """
    return render_template("exercise_1.html")


def main():
    """
    Runs the Flask app on host 0.0.0.0 and port 8080.

    This function is the main entry point for the application.
    """
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()
