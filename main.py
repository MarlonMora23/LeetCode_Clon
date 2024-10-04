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
database = os.path.join(basedir, "databases/users.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database}"
app.secret_key = os.environ.get("SECRET_KEY", "clave")
db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):
    user_id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(150), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(200), nullable=False)

    progresses = db.relationship("Progress", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Progress(db.Model):
    progress_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    problem_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(10000), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    solved = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Progress {self.progress_id} for User {self.user_id}>"


def get_problems() -> dict:
    """
    Returns a dictionary of IProblem instances, each representing one problem.

    The dictionary keys are the problem IDs and the values are instances of the
    corresponding IProblem class.

    Returns:
        dict: A dictionary of IProblem instances.
    """
    return {1: Problem1(), 2: Problem2(), 3: Problem3()}


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


def get_progress(user_progresses: list) -> list:
    progress_list = []

    for progress in user_progresses:
        progress_list.append({
            "problem_id": progress.problem_id,
            "code": progress.code,
            "language": progress.language,
            "solved": progress.solved
        })

    return progress_list

@app.route("/user/<int:user_id>/progress")
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

    # Obtener el progreso del usuario
    progress_list: list = Progress.query.filter_by(user_id=user_id).all()
    progress_data = [
        {"problem_id": p.problem_id, "code": p.code, "solved": p.solved, "language": p.language}
        for p in progress_list
    ]

    return jsonify(progress_data), 200


@app.route("/register-form")
def register_form():
    """
    Endpoint to render the registration form.

    The "next" query parameter can be used to specify the URL to redirect to after a successful registration.

    Returns a rendered HTML template of the registration form.

    :param next: The URL to redirect to after a successful registration.
    :type next: str

    :return: A rendered HTML template of the registration form.
    :rtype: str
    """
    next_url = request.args.get("next")

    return render_template("auth/register.html", next_url=next_url)


@app.route("/register", methods=["POST"])
def register():
    """
    Endpoint to register a new user using a JSON payload containing the username and password.

    The "next" query parameter can be used to specify the URL to redirect to after a successful registration.

    :param data: A JSON object containing the username and password of the new user.
    :type data: dict

    :return: A JSON response containing a message and a redirect URL if the registration is successful.
    :rtype: tuple
    """
    data: dict = request.get_json()
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Verify that the username and password fields are not empty
    if not username or not password or not confirm_password:
        return (
            jsonify(
                {
                    "message": "Nombre de usuario, contraseña y confirmar contraseña son requeridos"
                }
            ),
            400,
        )

    # Verify that the passwords match
    if password != confirm_password:
        return jsonify({"error": "Las contraseñas no coinciden"}), 400

    # Verify if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Nombre de usuario ya existe"}), 400

    # Create a new user in the database with hashed password
    hashed_password = generate_password_hash(password=password)
    new_user = User(username=username, password_hash=hashed_password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    next_url = data.get("next_url")

    if next_url == "None":
        next_url = url_for("home")

    return jsonify({"message": "Inicio de sesión con éxito", "redirect": next_url}), 200


@app.route("/login-form")
def login_form():
    """
    Endpoint to render the login form.

    The "next" query parameter can be used to specify the URL to redirect to after a successful login.

    Returns a rendered HTML template of the login form.

    :param next: The URL to redirect to after a successful login.
    :type next: str

    :return: A rendered HTML template of the login form.
    :rtype: str
    """
    next_url = request.args.get("next")

    return render_template("auth/login.html", next_url=next_url)


@app.route("/login", methods=["POST"])
def login():
    """
    Endpoint to login a user using a JSON payload containing the username and password.

    Returns a JSON response with a message and a redirect URL if the login is successful.
    The redirect URL is either the value of the "next" query parameter of the request or the home page.

    If the login is not successful, returns a JSON response with a message and a 401 status code.

    :param data: A JSON object containing the username and password of the user.
    :type data: dict

    :return: A JSON response containing a message and a redirect URL.
    :rtype: tuple
    """
    data: dict = request.get_json()
    user: User = User.query.filter_by(username=data["username"]).first()

    # Verify that the user exists and the password is correct
    if user and user.check_password(data["password"]):
        session["user_id"] = user.user_id
        session["username"] = user.username
        session['progress'] = get_progress(user.progresses)
        session['solved_problems'] = [progress.problem_id for progress in user.progresses if progress.solved]

        next_url = data.get("next_url")

        if next_url == "None":
            next_url = url_for("home")

        return (
            jsonify({"message": "Inicio de sesión con éxito", "redirect": next_url}),
            200,
        )

    return jsonify({"message": "Usuario o contraseña incorrecta"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    """
    Logs out the user by clearing the session.

    Returns:
        A JSON response with a message indicating that the logout was successful.
    """
    session.clear()  
    return jsonify({"message": "Logout successful"}), 200


def run_code(problem_id: int, code: str, language: str) -> tuple:
    """
    Runs a given code for a given problem and language.

    Args:
        problem_id (int): The id of the problem to be tested.
        code (str): The code to be tested.
        language (str): The programming language of the code (python or java).

    Returns:
        A tuple containing a JSON response and a status code.

        The JSON response contains the result of the test in JSON format with the following keys:

        - result: str,  # Exito/Fallo
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output

        The status code is either 200 (Success), 400 (Failure) or 404 (Problem not found or language not supported).

    Notes:
        This function assumes that the session has been initialized and contains the problem object.
        If any of the parameters is missing, it will return an error.
    """
    # Check if the session has been initialized and contains the problem object
    if "problem_object" not in session:
        return jsonify({"error": "Session no iniciada"}), 400

    if not problem_id or not language:
        return jsonify({"error": "Faltan datos"}), 400

    # Get the problem object
    problem_object: int = session["problem_object"]
    problem: IProblem = globals()[problem_object]()

    # Create a UserSubmission object
    submission = UserSubmission(problem_id, code, language)

    # Test the submission
    if problem_id in get_problems_ids():
        return test_problem(problem, submission)

    return jsonify({"error": "Problema no encontrado o lenguaje no soportado."}), 400


@app.route("/run", methods=["POST"])
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

    return run_code(problem_id, code, language)


@app.route("/submit", methods=["POST"])
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
    response: tuple = run_code(problem_id, code, language)
    solved: bool = response[1] == 201

    # Update the user's progress
    new_progress = Progress(
        user_id=user_id, problem_id=problem_id, code=code, solved=solved, language=language
    )
    db.session.add(new_progress)
    db.session.commit()

    return response


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
    user_id = session.get("user_id")
    user = db.session.get(User, user_id)

    # If the problem is valid, render the template
    if problem:
        session["problem_object"] = f"Problem{exercise_id}"

        if user:
            progress_list = Progress.query.filter_by(
                user_id=user.user_id, problem_id=exercise_id
            ).all()

            return render_template(
                f"exercises/exercise_{exercise_id}.html", problem=problem, progress_list=progress_list
            )

        return render_template(
            f"exercises/exercise_{exercise_id}.html", problem=problem
        )

    return "Ejercicio no encontrado", 404


@app.route("/home")
def home():
    """
    Handles a GET request to /home.

    Returns a rendered template with the list of available problems.
    """
    # Get the list of problems
    problems: list = [get_problem(i) for i in range(1, get_number_of_problems() + 1)]

    return render_template("home.html", problems=problems)


@app.route("/")
def index():
    """
    Handles a GET request to /.

    Returns the home page template with the list of problems.
    """
    return redirect(url_for("home"))


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
