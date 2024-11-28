"""
This module contains the Problem1 class, which represents all the features of 
the second exercise of the course.

The second exercise is to write a function that validates if a given password meets 
the requirements specified in the problem's metadata.

The Problem2 class implements the IProblem interface and provides a test list 
and expected output for the exercise.
"""

import re
from app.problem_solver.interfaces.i_problem import IProblem


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
        return "Escribe una función que valide una contraseña. Una contraseña es valida si contiene al menos una letra mayúscula, una letra minúscula, un número y un carácter especial."

    def get_detailed_problem_description(self) -> str:
        return "Escribe una función que valide una contraseña. Una contraseña es valida si contiene al menos una letra mayúscula, una letra minúscula, un número y un carácter especial. Escribe en la consola un programa que determine si una contraseña es valida o no. La función recibe una contraseña como argumento y devuelve Verdadero si la contraseña es valida, Falso si no lo es."
    
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
        ]
    
    def get_submission_test_list(self) -> list[str]:
        return [
            # Valid passwords
            "P@ssw0rd1",
            "Str0ngP@ssw0rd2",
            "L0ngP@ssw0rd3",
            "V@lidP@ssw0rd4",
            # Invalid passwords
            "short1!",  # Less than 8 characters
            "NOLOWERCASE1!",  # No lowercase letters
            "NoSpecial123",  # No special characters
            "NoDigits!",  # No numbers
            "",  # Empty password
            "12345678",  # Only numbers, no letters or special characters
            "abcdefgh",  # Only lowercase letters, no numbers or special characters
            "ABCDEFGH",  # Only uppercase letters, no numbers or special characters
            "!@#$%^&*()"
        ]

    def get_expected_output(self, submit: bool = False) -> list:
        """
        Returns a list of expected outputs for the problem.

        The expected output is a list of booleans indicating whether the password is valid or not.

        Returns:
            list: A list of expected outputs.
        """
        test_function: callable = self.get_test_function()
        test_list = self.get_test_list() if not submit else self.get_submission_test_list()

        return [test_function(password) for password in test_list]

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
    
    def get_ruby_function_name(self) -> str:
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Ruby.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Ruby.
        """
        return "validate_password"

    def get_test_function(self) -> callable:
        """
        Returns a function that tests if a given function is working correctly.

        Returns:
            callable: A function that takes a function as an argument and returns
            a list containing the result of the test for each test case.
        """

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

        return {
            "allow_recursion": False,
            "disallowed_keywords": ["__builtins__", "while"],
        }

    def get_initial_python_code(self) -> str:
        """
        Returns the initial Python code for the problem.

        Returns:
            str: The initial Python code for the problem.
        """
        return (
            "def validate_password(password: str) -> bool:\n"
            "    # Your code goes here\n"
            "    return None\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "public static boolean validatePassword(String n) {\n"
            "    // Your code goes here\n"
            "    return false;\n"
            "}\n"
        )
    
    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class validatePassword {\n"
            "    public static void main(String[] args) {\n"
            "        String n = String.valueOf(args[0]);\n"
            "        boolean result = validatePassword(n);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )
    
    def get_initial_ruby_code(self) -> str:
        """
        Returns the initial Ruby code for the problem.

        Returns:
            str: The initial Ruby code for the problem.
        """
        return (
            "def validate_password(password)\n"
            "    # Your code goes here\n"
            "    return false\n"
            "end\n"
        )
    
    def get_testing_ruby_code(self) -> str:
        return (
            "input = ARGV[0]\n"
            "result = validate_password(input)\n"
            "puts result\n"
        )
    
    def is_boolean(self):
        return True
    
    def is_integer(self):
        return False
    
