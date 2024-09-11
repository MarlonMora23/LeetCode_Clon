"""
This module contains some abstracted functions to test Python and Java code.
"""

import ast
import re


def is_problem_python_function_defined(
    local_vars: dict, expected_function_name: str
) -> bool:
    """
    Checks if a Python function is defined in the given local variables.

    Args:
        local_vars: A dictionary containing the local variables of the function's scope.
        expected_function_name: The expected name of the function to be tested.

    Returns:
        A boolean indicating whether the function is defined or not.
    """
    if expected_function_name not in local_vars:
        return False

    return True


def is_problem_java_function_defined(
    file_path: str, expected_function_name: str
) -> bool:
    """
    Checks if a Java function is defined in the given file.

    Args:
        file_path: The path to the Java file.
        expected_function_name: The expected name of the function to be tested.

    Returns:
        A boolean indicating whether the function is defined or not.
    """
    try:
        with open(f"{file_path}.java", "r") as file:
            java_code: str = file.read()

            return f"public static boolean {expected_function_name}" in java_code

    except FileNotFoundError:
        return False


def validate_recursion_python(code: str, problem: dict) -> dict:
    """
    Validates if a given Python code does not use recursion if it is not allowed.

    Args:
        code: The Python code to be tested.
        problem: A dictionary containing information about the problem, including
            whether recursion is allowed.

    Returns:
        A dictionary containing the test results, including success status and
        feedback.
    """
    if not problem["allow_recursion"]:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and any(
                isinstance(child, ast.Call) and child.func.id == node.name
                for child in ast.walk(node)
            ):
                return {
                    "result": "Failure",
                    "feedback": "La función no debe usar recursión.",
                }

    return {"result": "Success"}


def validate_recursion_java(
    code: str, problem: dict, expected_function_name: str
) -> dict:
    """
    Validates if a given Java code does not use recursion if it is not allowed.

    Args:
        code: The Java code to be tested.
        problem: A dictionary containing information about the problem, including
            whether recursion is allowed.
        expected_function_name: The expected name of the function to be tested.

    Returns:
        A dictionary containing the test results, including success status and
        feedback.
    """
    if not problem["allow_recursion"]:
        matches = re.findall(expected_function_name, code)

        if len(matches) > 2:
            return {
                "result": "Failure",
                "feedback": "La función no debe usar recursión.",
            }

        return {"result": "Success"}

    return {"result": "Success"}


def validate_metadata(
    code: str,
    metadata: dict,
    problem_id: int,
    language: str,
    expected_function_name: str,
) -> dict:
    """
    Validates if a given code meets the requirements specified in the problem's metadata.

    Args:
        code: The code to be tested.
        metadata: A dictionary containing information about the problem.
        problem_id: The ID of the problem.
        language: The language of the code.
        expected_function_name: The expected name of the function in the code.

    Returns:
        A dictionary containing the test results, including success status and
        feedback.
    """
    problem: dict = metadata.get(problem_id)

    # Verify if the code contains disallowed keywords
    for keyword in problem["disallowed_keywords"]:
        if keyword in code:
            return {
                "result": "Failure",
                "feedback": "El código contiene palabras no permitidas.",
            }

    # Verify if the code uses recursion
    if language == "python":
        return validate_recursion_python(code, problem)

    if language == "java":
        return validate_recursion_java(code, problem, expected_function_name)


def get_metadata() -> dict:
    """
    Returns a dictionary containing metadata about the problems.

    The dictionary maps problem IDs to another dictionary containing two keys:

    - "allow_recursion": A boolean indicating whether recursion is allowed in the solution.
    - "disallowed_keywords": A list of keywords that should not be used in the solution.

    """
    return {
        1: {"allow_recursion": False, "disallowed_keywords": ["while"]},
        2: {"allow_recursion": False, "disallowed_keywords": []},
        3: {"allow_recursion": False, "disallowed_keywords": []},
    }
