"""
This module contains the Problem1 class, which represents all the features of 
the first exercise of the course.

The first exercise is to write a function that determines if a number is prime or not.
A prime number is a natural number greater than 1 that has no positive divisors
other than 1 and itself.

The Problem1 class implements the IProblem interface and provides a test list and
expected output for the exercise.
"""

import subprocess
from problem_solver.user_submission import UserSubmission
from problem_solver.i_problem import IProblem


def is_prime_number(n: int) -> bool:
    """
    Returns True if n is a prime number, False otherwise.
    A prime number is a natural number greater than 1 that has no positive divisors
    other than 1 and itself.

    This function uses the square root optimization to check if a number is prime.
    Time complexity: O(sqrt(n))
    """
    if n <= 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


class Problem1(IProblem):
    """
    The Problem1 class represents the first exercise of the course.

    The first exercise is to write a function that determines if a number is prime or not.
    A prime number is a natural number greater than 1 that has no positive divisors
    other than 1 and itself.

    The Problem1 class implements the IProblem interface and provides a test list and
    expected output for the exercise.
    """

    def get_problem_id(self) -> int:
        """
        Returns the id of the problem.

        Returns:
            int: The id of the problem.
        """
        return 1

    def get_test_list(self) -> list:
        """
        Returns a list of test cases for the problem.

        Returns:
            list: A list of test cases.
        """

        return [3, 4, 7, 10, 11, 12, 19, 20, 23, 24, 29, 33, 37]

    def get_target(self) -> None:
        """
        Returns the target of the problem.

        Returns:
            None: No target required for prime number check
        """
        return None  # No target required for prime number check

    def get_expected_output(self) -> list:
        """
        Returns a list of expected outputs for the problem.

        The expected output is a list of booleans indicating whether the number is prime or not.

        Returns:
            list: A list of expected outputs.
        """
        test_function: callable = self.get_test_function()

        return [test_function(i) for i in self.get_test_list()]

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
        return "is_prime_number"

    def get_java_function_name(self) -> str:
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Java.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Java.
        """
        return "isPrimeNumber"

    def get_test_function(self) -> callable:
        """
        Returns a function that tests if a given function is working correctly.

        Returns:
            callable: A function that takes a function as an argument and returns
            a list containing the result of the test for each test case.
        """

        return is_prime_number

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
        Returns the initial Python code for the problem, formatted in a way
        that improves readability.

        Returns:
            str: The initial Python code for the problem.
        """
        return (
            "def is_prime_number(n: int) -> bool:\n"
            '    """\n'
            "    Checks if a given number is a prime number.\n\n"
            "    Parameters\n"
            "    ----------\n"
            "    n : int\n"
            "        The number to be checked for primality.\n\n"
            "    Returns\n"
            "    -------\n"
            "    bool\n"
            "        True if the number is a prime number, False otherwise.\n"
            '    """\n'
            "    return None\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem, formatted for improved readability.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "package temp;\n\n"
            "public class isPrimeNumber {\n"
            "    public static void main(String[] args) {      \n"
            "        int n = Integer.parseInt(args[0]);        \n"
            "        boolean result = isPrimeNumber(n);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
            "    public static boolean isPrimeNumber(int n) {\n"
            "        // Your code goes here\n"
            "        return false;\n"
            "    }\n"
            "}\n"
        )
