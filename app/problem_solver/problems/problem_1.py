"""
This module contains the Problem1 class, which represents all the features of 
the first exercise of the course.

The first exercise is to write a function that determines if a number is prime or not.
A prime number is a natural number greater than 1 that has no positive divisors
other than 1 and itself.

The Problem1 class implements the IProblem interface and provides a test list and
expected output for the exercise.
"""

from app.problem_solver.interfaces.i_problem import IProblem


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
        Returns:
            int: The id of the problem.
        """
        return 1

    def get_problem_name(self) -> str:
        """
        Returns:
            str: The name of the problem.
        """
        return "¿Es primo?"

    def get_problem_description(self) -> str:
        """
        Returns:
            str: The description of the problem.
        """
        return "Escribe una función que determina si un número es primo o no. Un número primo es un número natural mayor que 1 que no tiene divisores positivos otros que 1 y el mismo."

    def get_detailed_problem_description(self) -> str:
        return "Un número primo es un número natural mayor que 1 que no tiene divisores positivos otros que 1 y el mismo. Escribe en la consola un programa que determine si un número es primo o no. La función recibe un número como argumento y devuelve Verdadero si el número es primo, Falso si no lo es."

    def get_problem_difficulty(self) -> str:
        """
        Returns:
            str: The difficulty of the problem.
        """
        return "easy"

    def get_test_list(self) -> list:
        """
        Returns:
            list: A list of test cases.
        """

        return [3, 4, 7, 10, 11, 12, 19, 20, 23, 24, 29, 33, 37]

    def get_submission_test_list(self) -> list:
        return [n for n in range(2, 1000) if n % 2 == 1]

    def get_expected_output(self, submit: bool = False) -> list:
        """
        Returns a list of expected outputs for the problem.

        The expected output is a list of booleans indicating whether the number is prime or not.

        Returns:
            list: A list of expected outputs.
        """
        test_function: callable = self.get_test_function()
        test_list = (
            self.get_test_list() if not submit else self.get_submission_test_list()
        )

        return [test_function(i) for i in test_list]

    def get_python_function_name(self) -> str:
        """
        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Python.
        """
        return "is_prime_number"

    def get_java_function_name(self) -> str:
        """
        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Java.
        """
        return "isPrimeNumber"

    def get_ruby_function_name(self) -> str:
        """
        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Ruby.
        """
        return "is_prime_number"

    def get_test_function(self) -> callable:
        """
        Returns a function that tests if a given function is working correctly.

        Returns:
            callable: A function that takes a function as an argument and returns
            a list containing the result of the test for each test case.
        """

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
            "    # Your code goes here\n"
            "    return None\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem, formatted for improved readability.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "public static boolean isPrimeNumber(int n) {\n"
            "    // Your code goes here\n"
            "    return false;\n"
            "}\n"
        )

    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class isPrimeNumber {\n"
            "    public static void main(String[] args) {      \n"
            "        int n = Integer.parseInt(args[0]);        \n"
            "        boolean result = isPrimeNumber(n);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )

    def get_initial_ruby_code(self) -> str:
        """
        Returns the initial Ruby code for the problem, formatted for improved readability.

        Returns:
            str: The initial Ruby code for the problem.
        """
        return (
            "def is_prime_number(n)\n"
            "    # Your code goes here\n"
            "    return false\n"
            "end\n"
        )

    def get_testing_ruby_code(self) -> str:
        return (
            "input = ARGV[0].to_i\n" "result = is_prime_number(input)\n" "puts result\n"
        )

    def is_boolean(self):
        return True

    def is_integer(self):
        return False
