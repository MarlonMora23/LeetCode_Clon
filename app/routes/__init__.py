from .main import main_blueprint
from .auth import auth_blueprint
from .user_submission import user_submission_blueprint


def register_routes(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_submission_blueprint)
