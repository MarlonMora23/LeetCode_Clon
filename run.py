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
from app import create_app
from app.routes import register_routes

class RunApp:
    def __init__(self):
        """
        Runs the Flask app on host 0.0.0.0 and port 8080.

        This function is the main entry point for the application.
        """
        self.app = create_app()
        register_routes(self.app)
        self.app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    RunApp()
