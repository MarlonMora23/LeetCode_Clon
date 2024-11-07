"""
This module contains the Problem1 class, which represents all the features of 
the second exercise of the course.

The second exercise is to write a function that validates if a given password meets 
the requirements specified in the problem's metadata.

The Problem2 class implements the IProblem interface and provides a test list 
and expected output for the exercise.
"""

import re
import subprocess
from problem_solver.user_submission import UserSubmission
from problem_solver.i_problem import IProblem


def validate_password(password: str) -> bool:
    """
    Validates if a given password meets the requirements specified in the problem's metadata.

    Args:
        password: The password to be tested.

    Returns:
        A boolean indicating whether the password is valid or not.
    """
    # At least 8 characters
    if len(password) < 8:
        return False

    # At least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # At least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False

    # At least one digit
    if not re.search(r"\d", password):
        return False

    # At least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


class Problem2(IProblem):
    """
    Represents the second problem of the course.

    The second problem is to write a function that validates a given password.
    The function should return True if the password is valid, and False otherwise.
    A valid password must contain at least one uppercase letter, at least one lowercase letter,
    at least one digit, and at least one special character.
    """

    def get_problem_id(self) -> int:
        """
        Returns the id of the problem.

        Returns:
            int: The id of the problem.
        """
        return 2
    
    def get_problem_name(self) -> str:
        """
        Returns:
            str: The name of the problem.
        """
        return "Validar contraseña"
    
    def get_problem_description(self) -> str:
        """
        Returns:
            str: The description of the problem.
        """
        return "Escribe una función que valide una contraseña. Una contraseña es valida si contiene al menos una letra mayúscula, al menos una letra minúscula, al menos un número y al menos un carácter especial."
    
    def get_problem_difficulty(self) -> str:
        """
        Returns:
            str: The difficulty of the problem.
        """
        return "easy"

    def get_test_list(self) -> list[str]:
        """
        Returns a list of test cases for the problem.

        The list contains valid and invalid passwords to be tested.

        Returns:
            list: A list of test cases.
        """
        return [
            # Valid passwords
            "Password1!",
            "Valid123$",
            "Str0ngP@ssw0rd",
            # Invalid passwords
            "short1!",  # Less than 8 characters
            "nouppercase1!",  # No uppercase letters
            "NOLOWERCASE1!",  # No lowercase letters
            "NoSpecial123",  # No special characters
            "NoDigits!",  # No numbers
            "",  # Empty password
            "12345678",  # Only numbers, no letters or special characters
            "abcdefgh",  # Only lowercase letters, no numbers or special characters
            "ABCDEFGH",  # Only uppercase letters, no numbers or special characters
            "!@#$%^&*()",
        ]

    def get_target(self) -> any:
        """
        Returns the target of the problem.

        Returns:
            any: The target of the problem. In this case, None is returned because
            no target is required for password validation.
        """
        return None  # No target required for password validation

    def get_expected_output(self) -> list:
        """
        Returns a list of expected outputs for the problem.

        The expected output is a list of booleans indicating whether the password is valid or not.

        Returns:
            list: A list of expected outputs.
        """
        test_function: callable = self.get_test_function()

        return [test_function(password) for password in self.get_test_list()]

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
        tested_output: list = []
        if user_submission.language == "python":
            local_vars: dict = user_code
            user_function: callable = local_vars[self.get_python_function_name()]

            for test_number in self.get_test_list():
                tested_output.append(user_function(test_number))

            return tested_output

        if user_submission.language == "java":
            temp_file_path: str = user_code

            for test_number in self.get_test_list():
                run_process = subprocess.run(
                    ["java", temp_file_path, str(test_number)],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                java_result: str = run_process.stdout.strip()
                result: bool = java_result == "true"
                tested_output.append(result)

            return tested_output

        raise ValueError(f"Unsupported language: {user_submission.language}")

    def get_python_function_name(self) -> str:
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Python.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Python.
        """
        return "validate_password"

    def get_java_function_name(self) -> str:
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Java.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Java.
        """
        return "validatePassword"

    def get_test_function(self) -> callable:
        """
        Returns a function that tests if a given function is working correctly.

        Returns:
            callable: A function that takes a function as an argument and returns
            a list containing the result of the test for each test case.
        """
        return validate_password

    def get_metadata(self) -> dict:
        """
        Returns a dictionary containing metadata about the problem.

        The dictionary should contain the following keys:

        - allow_recursion (bool): Whether the problem allows recursion.
        - disallowed_keywords (list[str]): A list of keywords that are not allowed in the solution.

        Returns:
            dict: A dictionary containing the metadata about the problem.
        """

        return {"allow_recursion": False, "disallowed_keywords": ["__builtins__", "while"],}

    def get_initial_python_code(self) -> str:
        """
        Returns the initial Python code for the problem.

        Returns:
            str: The initial Python code for the problem.
        """
        return (
            "def validate_password(password: str) -> bool:\n"
            '    """\n'
            "    Validates if a given password meets the requirements "
            "       specified in the problem's metadata.\n\n"
            "    Args:\n"
            "        password: The password to be tested.\n\n"
            "    Returns:\n"
            "        A boolean indicating whether the password is valid or not.\n"
            '    """\n'
            "    return None\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "package temp;\n\n"
            "public class validatePassword {\n"
            "    public static void main(String[] args) {\n"
            "        String n = String.valueOf(args[0]);\n"
            "        boolean result = validatePassword(n);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
            "    public static boolean validatePassword(String n) {\n"
            "        // Your code goes here\n"
            "        return false;\n"
            "    }\n"
            "}\n"
        )
