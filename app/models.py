from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    def __init__(self):
        """
        Initializes the database.

        This method initializes the database by creating an instance of the SQLAlchemy class.

        The instance is stored in the `db` attribute of the class.

        Returns:
            None
        """
        self.db: SQLAlchemy = SQLAlchemy()

    def init_app(self, app):
        """
        Initializes the database with the given Flask application.

        This method initializes the database with the given Flask application by calling
        the `init_app` method of the SQLAlchemy instance.

        The method also creates all the tables in the database by calling the
        `create_all` method of the SQLAlchemy instance.

        Args:
            app: The Flask application to initialize the database with.

        Returns:
            None
        """
        self.db.init_app(app)

        with app.app_context():
            self.db.create_all()

    def get_instance(self):
        """
        Returns the instance of the database.

        This method returns the instance of the database created by the constructor.

        Returns:
            SQLAlchemy: The instance of the database.
        """
        return self.db


database: Database = Database()
db: SQLAlchemy = database.get_instance()


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
