"""
app package.

This package contains the main Flask application and its configuration.
"""

import os
from flask import Flask
from app.models import database as db

def create_app():
    """
    Creates a Flask application instance.

    This function creates a Flask application instance and configures the database
    URI and secret key. It also initializes the database.

    Returns:
        Flask: The Flask application instance.
    """
    app: Flask = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    database = os.path.join(basedir, "databases/users.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database}"
    app.secret_key = os.environ.get("SECRET_KEY", "clave")
    db.init_app(app)

    return app
