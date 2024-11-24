from flask import Blueprint, jsonify, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db
from app.models import User
from app.utils import get_progress

auth_blueprint = Blueprint("auth", __name__)
HOME_URL = "main.home"


@auth_blueprint.route("/register-form")
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


@auth_blueprint.route("/register", methods=["POST"])
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
    username: str = data.get("username")
    password: str = data.get("password")
    confirm_password: str = data.get("confirm_password")

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
        next_url = url_for(HOME_URL)

    return jsonify({"message": "Inicio de sesión con éxito", "redirect": next_url}), 200


@auth_blueprint.route("/login-form")
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
    # Get the next URL from the query string, defaulting to the home page
    next_url = request.args.get("next", url_for(HOME_URL))

    return render_template("auth/login.html", next_url=next_url)


@auth_blueprint.route("/login", methods=["POST"])
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
        session["progress"] = get_progress(user.progresses)
        session["solved_problems"] = [
            progress.problem_id for progress in user.progresses if progress.solved
        ]

        # Get the next URL from the query string, defaulting to the home page
        next_url = data.get("next_url") or url_for(HOME_URL)

        return (
            jsonify({"message": "Inicio de sesión con éxito", "redirect": next_url}),
            200,
        )

    return jsonify({"message": "Usuario o contraseña incorrecta"}), 401


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    """
    Logs out the user by clearing the session.

    Returns:
        A JSON response with a message indicating that the logout was successful.
    """
    session.clear()
    return jsonify({"message": "Logout successful"}), 200
