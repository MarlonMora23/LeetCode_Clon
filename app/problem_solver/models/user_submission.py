"""
This module contains the UserSubmission class, which represents a user's submission to a problem. 
"""


class UserSubmission:
    """
    Represents a user's submission to a problem.

    Attributes:
        problem_id (int): The id of the problem the user submitted a solution for.
        code (str): The code submitted by the user.
        language (str): The programming language used by the user.
    """

    def __init__(self, problem_id: int, code: str, language: str):
        """
        Initializes a UserSubmission object.

        Args:
            problem_id (int): The id of the problem the user submitted a solution for.
            code (str): The code submitted by the user.
            language (str): The programming language used by the user.
        """
        self.problem_id: int = problem_id
        self.code: str = code
        self.language: str = language

    def get_problem_id(self) -> int:
        """
        Returns the id of the problem the user submitted a solution for.
        """
        return self.problem_id

    def get_code(self) -> str:
        """
        Returns the code submitted by the user.
        """
        return self.code

    def get_language(self) -> str:
        """
        Returns the programming language used by the user.
        """
        return self.language
