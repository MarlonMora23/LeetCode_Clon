import os
from flask import Flask
from app.models import database as db

def create_app():
    app: Flask = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    database = os.path.join(basedir, "databases/users.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database}"
    app.secret_key = os.environ.get("SECRET_KEY", "clave")
    db.init_app(app)

    return app
