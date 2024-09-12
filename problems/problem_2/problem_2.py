import re
from problems.MyApp import test_problem
from problems.i_problem import IProblem


class Problem2(IProblem):
    def get_problem_id(self) -> int:
        return 2

    def get_test_list(self) -> list[str]:
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
        return None  # No target required for password validation
    
    def get_n_test_cases(self) -> int:
        return 1

    def get_python_function_name(self) -> str:
        return "validate_password"

    def get_java_function_name(self) -> str:
        return "validatePassword"

    def get_test_function(self) -> callable:
        return validate_password


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

    # At least one digit
    if not re.search(r"\d", password):
        return False

    # At least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


def test_problem_2(data: dict) -> tuple:
    """
    Tests problem 1 in the given language.

    Args:
        data: A dictionary containing the code to be tested and the language.

    Returns:
        A tuple containing the result of the test in JSON format and a status code.
    """
    problem = Problem2()
    return test_problem(problem, data)
