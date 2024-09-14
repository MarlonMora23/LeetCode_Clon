"""
This module contains the IProblem class, which is an abstract base class for problems.
A problem is represented by a class that implements this interface.
The class must implement the abstract methods defined in this interface.
"""

# pylint: disable=unnecessary-pass

from abc import ABC, abstractmethod
from problem_solver.user_submission import UserSubmission


class IProblem(ABC):
    """
    Interface for a problem.

    A problem is represented by a class that implements this interface.
    The class must implement the abstract methods defined in this interface.
    """

    @abstractmethod
    def get_problem_id(self) -> int:
        """
        Returns the id of the problem.

        Returns:
            int: The id of the problem.
        """
        pass

    @abstractmethod
    def get_test_list(self) -> list:
        """
        Returns a list of test cases for the problem.

        Returns:
            list: A list of test cases.
        """
        pass

    @abstractmethod
    def get_expected_output(self) -> list:
        """
        Returns a list of expected outputs for the problem.

        Returns:
            list: A list of expected outputs.
        """
        pass

    @abstractmethod
    def test_user_submission(
        self, user_code: dict | str, user_submission: UserSubmission
    ) -> list:
        """
        Tests if a given function is working correctly.

        Args:
            user_code: The user's code to be tested. Could be a dictionary if the language
                is Python, or a string if the language is Java.
            user_submission: An UserSubmission instance containing the user's code and the language.

        Returns:
            A list containing the result of the test for each test case.
        """

        pass

    @abstractmethod
    def get_target(self) -> any:
        """
        Returns the target of the problem.

        Returns:
            any: The target of the problem.
        """

        pass

    @abstractmethod
    def get_python_function_name(self) -> str:
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Python.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Python.
        """
        pass

    @abstractmethod
    def get_java_function_name(self) -> str:
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Java.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Java.
        """

        pass

    @abstractmethod
    def get_test_function(self) -> callable:
        """
        Returns a function that tests if a given function is working correctly.

        Returns:
            callable: A function that takes a function as an argument and returns
            a list containing the result of the test for each test case.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> dict:
        """
        Returns a dictionary containing metadata about the problem.

        The dictionary should contain the following keys:

        - allow_recursion (bool): Whether the problem allows recursion.
        - disallowed_keywords (list[str]): A list of keywords that are not allowed in the solution.

        Returns:
            dict: A dictionary containing the metadata about the problem.
        """

        pass

    @abstractmethod
    def get_initial_python_code(self) -> str:
        """
        Returns the initial Python code for the problem.

        Returns:
            str: The initial Python code for the problem.
        """
        pass

    @abstractmethod
    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem.

        Returns:
            str: The initial Java code for the problem.
        """
        pass
