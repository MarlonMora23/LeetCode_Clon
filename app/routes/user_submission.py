from flask import Blueprint, jsonify, render_template, request, session
from app.models import Progress, User
from app.utils import get_progress, run_code
from app.models import Progress, User
from app.models import db
from app.utils import get_number_of_problems, get_problem, get_supported_languages, get_language_codes


user_submission_blueprint = Blueprint("user_submission", __name__)

@user_submission_blueprint.route("/exercise/<int:exercise_id>")
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
    has_target = hasattr(problem, "get_target")
    supported_languages = get_supported_languages()
    problems_length = get_number_of_problems()
    user_id = session.get("user_id")
    user = db.session.get(User, user_id)

    # If the problem is valid, render the template
    if problem:
        session["problem_object"] = f"Problem{exercise_id}"

        if user:
            progress_list = Progress.query.filter_by(
                user_id=user.user_id, problem_id=exercise_id
            ).all()
            last_codes = None

            if progress_list:
                last_codes = {}
                for progress in progress_list:
                    if progress.solved and problem.get_problem_id() == progress.problem_id:
                        last_codes[progress.language] = progress.code

                language_codes = get_language_codes(problem, last_codes)

                return render_template(
                    "exercises/exercise_base.html",
                    problem=problem,
                    has_target=has_target,
                    progress_list=progress_list,
                    problems_length=problems_length,
                    language_codes=language_codes,
                    supported_languages=supported_languages
                )

        language_codes = get_language_codes(problem)
        return render_template(
            "exercises/exercise_base.html",
            problem=problem,
            has_target=has_target,
            problems_length=problems_length,
            language_codes=language_codes,
            supported_languages=supported_languages
        )

    return "Ejercicio no encontrado", 404


@user_submission_blueprint.route("/user/<int:user_id>/progress")
def get_user_progress(user_id):
    """
    Endpoint to get the progress of a user.

    The user's progress is returned as a JSON object containing a list of the user's progress for each problem.
    Each item in the list contains the problem ID, the code, whether the problem is solved, and the language used.

    Args:
        user_id (int): The ID of the user.

    Returns:
        A JSON object containing the user's progress for each problem.
    """
    user: User = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    # Get user progress
    progress_list: list = Progress.query.filter_by(user_id=user_id).all()
    progress_data = [
        {
            "problem_id": p.problem_id,
            "code": p.code,
            "solved": p.solved,
            "language": p.language,
        }
        for p in progress_list
    ]

    return jsonify(progress_data), 200


@user_submission_blueprint.route("/run", methods=["POST"])
def run() -> tuple:
    """
    Handles a POST request to /run, which should contain a JSON payload
    with the following structure:

    {
        "problem_id": int,
        "code": str,
        "language": str
    }

    Returns a tuple containing a JSON Response object and a status code.
    The JSON Response object contains the result of the test with the following keys:

    - result: str,  # Exito/Fallo
    - feedback: str,  # Feedback for the user
    - expected_output: list,  # Expected output
    - tested_output: list  # User's output

    The status code is either 200 (Success) or 400 (Failure).
    """
    data: dict = request.get_json()
    problem_id = data.get("problem_id")
    code = data.get("code")
    language = data.get("language")

    return run_code(problem_id, code, language, False)


@user_submission_blueprint.route("/submit", methods=["POST"])
def submit():
    """
    Handles a POST request to /submit, which should contain a JSON payload
    with the following structure:

    {
        "problem_id": int,
        "code": str,
        "language": str
    }

    If the user is not logged in, returns a JSON object with a single key
    "error" set to "Para subir una solución, primero inicia sesión.", and
    a status code of 400.

    If the request is invalid (e.g. missing fields), returns a JSON object
    with a single key "error" set to "Invalid request", and a status code of 400.

    If the language is unsupported, returns a JSON object with a single key
    "error" set to "Unsupported language", and a status code of 400.

    If the code is correct, returns a JSON object with a single key
    "result" set to "Success", and a status code of 201.

    If the code is incorrect, returns a JSON object with a single key
    "result" set to "Failure", and a status code of 400.

    Also, updates the user's progress in the database.
    """
    user_id = session.get("user_id")
    user: User = db.session.get(User, user_id)

    if not user:
        return (
            jsonify({"error": "Para subir una solución, primero inicia sesión."}),
            400,
        )

    # Get the data from the request
    data: dict = request.get_json()
    problem_id: int = data.get("problem_id")
    code: str = data.get("code")
    language: str = data.get("language")

    # Run the code and verify if it was successful
    response: tuple = run_code(problem_id, code, language, True)
    solved: bool = response[1] == 201

    # Update the user's progress
    new_progress = Progress(
        user_id=user_id,
        problem_id=problem_id,
        code=code,
        solved=solved,
        language=language,
    )
    db.session.add(new_progress)
    db.session.commit()

    session["progress"] = get_progress(user.progresses)
    session["solved_problems"] = [
        progress.problem_id for progress in user.progresses if progress.solved
    ]

    return response
