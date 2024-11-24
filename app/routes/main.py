from flask import Blueprint, redirect, render_template, url_for
from app.utils import get_number_of_problems, get_problem

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/home")
def home():
    """
    Handles a GET request to /home.

    Returns a rendered template with the list of available problems.
    """
    # Get the list of problems
    problems: list = [get_problem(i) for i in range(1, get_number_of_problems() + 1)]

    return render_template("home.html", problems=problems)


@main_blueprint.route("/")
def index():
    """
    Handles a GET request to /.

    Returns the home page template with the list of problems.
    """
    return redirect(url_for("main.home"))
