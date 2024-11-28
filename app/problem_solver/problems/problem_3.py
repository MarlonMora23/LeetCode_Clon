"""
This module contains the Problem3 class, which represents the third exercise of the course.

The third exercise is to write a function that searches for a target in an array and returns
True if found, False otherwise.

The Problem3 class implements the IProblem interface and provides a test list and expected
output for the exercise.
"""

from app.problem_solver.interfaces.i_problem import IProblem


class Problem3(IProblem):
    """
    Represents the third exercise of the course.

    The third exercise is to write a function that searches for a target in an array and returns
    True if found, False otherwise.

    The Problem3 class implements the IProblem interface and provides a test list and expected
    output for the exercise.
    """

    def get_problem_id(self) -> int:
        """
        Returns the id of the problem.

        Returns:
            int: The id of the problem.
        """

        return 3

    def get_problem_name(self) -> str:
        """
        Returns:
            str: The name of the problem.
        """
        return "Buscar un número"

    def get_problem_description(self) -> str:
        """
        Returns:
            str: The description of the problem.
        """
        return "Escribe una función que busca un número en un arreglo y devuelve Verdadero si lo encuentra, Falso si no lo encuentra."
    
    def get_detailed_problem_description(self) -> str:
        return "Escriba una funcion que busque un numero en un arreglo y devuelva verdadero si lo encuentra, o falso si no lo encuentra. La función recibe dos arguementos, un arreglo y un numero, y devuelve verdadero si lo encuentra, o falso si no lo encuentra. En el ejemplo, la primera entrada es la lista de números y la segunda entrada es la lista de numeros a buscar. Ten en cuenta que aunque la segunda entrada es una lista en el ejemplo, se enviará un número por iteración."

    def get_problem_difficulty(self) -> str:
        """
        Returns:
            str: The difficulty of the problem.
        """
        return "easy-medium"

    def get_test_list(self) -> list:
        """
        Returns a list of test cases for the problem.

        Returns:
            list: A list of test cases.
        """
        return [3, 4, 7, 10, 11, 12, 19, 20, 23, 24, 29, 33, 37]
    
    def get_submission_test_list(self) -> list:
        return [n for n in range(2, 1000) if n % 2 == 1]

    def get_target(self) -> any:
        """
        Returns the target of the problem.

        Returns:
            any: The target of the problem.
        """
        return [3, 5, 12, 22, 37]
    
    def get_submission_target(self) -> any:
        return [n for n in range(2, len(self.get_submission_test_list()) * 7, 7) if n % 2 == 1]

    def get_expected_output(self, submit: bool) -> list:
        """
        Returns a list of expected outputs for the problem.

        The expected output is a list of booleans indicating whether the target
        is found in the array or not.

        Returns:
            list: A list of expected outputs.
        """
        test_function: callable = self.get_test_function()
        test_list = self.get_test_list() if not submit else self.get_submission_test_list()
        target = self.get_target() if not submit else self.get_submission_target()

        return [test_function(test_list, target) for target in target]

    def get_python_function_name(self) -> str:
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Python.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Python.
        """
        return "search_number"

    def get_java_function_name(self) -> str:
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Java.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Java.
        """
        return "searchNumber"
    
    def get_ruby_function_name(self):
        """
        Returns the name of the function in the problem that is expected
        to be implemented in Ruby.

        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Ruby.
        """
        return "search_number"

    def get_test_function(self) -> callable:
        """
        Returns a function that tests if a given function is working correctly.

        Returns:
            callable: A function that takes a function as an argument and returns
            a list containing the result of the test for each test case.
        """

        def search_number(array: list, target: int):
            """
            Searches for a target in an array and returns True if found, False otherwise

            Parameters
            ----------
            array : list
                The array to search in
            target : int
                The target to search for

            Returns
            -------
            bool
                True if the target is found in the array, False otherwise
            """
            return target in array

        return search_number

    def get_metadata(self) -> dict:
        """
        Returns a dictionary containing metadata about the problem.

        The dictionary should contain the following keys:

        - allow_recursion (bool): Whether the problem allows recursion.
        - disallowed_keywords (list[str]): A list of keywords that are not allowed in the solution.

        Returns:
            dict: A dictionary containing the metadata about the problem.
        """
        return {"allow_recursion": False, "disallowed_keywords": ["__builtins__"]}

    def get_initial_python_code(self) -> str:
        """
        Returns the initial Python code for the problem.

        The initial code is a docstring with a description of the problem and
        a function signature with a return type and parameters.

        Returns:
            str: The initial Python code for the problem.
        """
        return (
            "def search_number(array: list, target: int):\n"
            "    # Your code goes here\n"
            "    return None\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem.

        The initial code is a docstring with a description of the problem and
        a function signature with a return type and parameters.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "public static boolean searchNumber(int[] array, int target) {\n"
            "    // Your code goes here\n"
            "    return false;\n"
            "}\n"
        )
    
    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class searchNumber {\n"
            "    public static void main(String[] args) {\n"
            "        String[] stringArray = args[0].split(\",\");\n"
            "        int[] array = new int[stringArray.length];\n"
            "        for (int i = 0; i < stringArray.length; i++) {\n"
            "            array[i] = Integer.parseInt(stringArray[i]);\n"
            "        }\n\n"
            "        int target = Integer.parseInt(args[1]);\n"
            "        boolean result = searchNumber(array, target);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )
    
    def get_initial_ruby_code(self) -> str:
        """
        Returns the initial Ruby code for the problem.

        The initial code is a docstring with a description of the problem and
        a function signature with a return type and parameters.

        Returns:
            str: The initial Ruby code for the problem.
        """
        return (
            "def search_number(array, target)\n"
            "    # Your code goes here\n"
            "    return false\n"
            "end\n"
        )
    
    def get_testing_ruby_code(self) -> str:
        return (
            "array = ARGV[0].split(',').map(&:to_i)\n"
            "target = ARGV[1].to_i\n"
            "result = search_number(array, target)\n"
            "puts result\n"
        )
    
    def is_boolean(self):
        return True
    
    def is_integer(self):
        return False
    
