"""
This module contains functions to test Python and Java code.

The functions in this module are responsible for compiling and testing the code
submitted by the user. The functions take an IProblem instance and a UserSubmission
instance as parameters, and return a dictionary containing the result of the test
in JSON format.

The functions in this module are used by the main application to test code
submitted by the user.
"""

import ast
import os
import re
import subprocess
from flask import Response, jsonify
from problem_solver.i_problem import IProblem
from problem_solver.user_submission import UserSubmission


def is_problem_python_function_defined(local_vars: dict, function_name: str) -> bool:
    """
    Checks if a Python function is defined in the given local variables.

    Args:
        local_vars: A dictionary containing the local variables of the function's scope.
        function_name: The expected name of the function to be tested.

    Returns:
        A boolean indicating whether the function is defined or not.
    """
    if function_name not in local_vars:
        return False

    return True


def is_problem_java_function_defined(file_path: str, function_name: str) -> bool:
    """
    Checks if a Java function is defined in the given file.

    Args:
        file_path: The path to the Java file.
        function_name: The expected name of the function to be tested.

    Returns:
        A boolean indicating whether the function is defined or not.
    """
    try:
        with open(f"{file_path}.java", "r", encoding="utf-8") as file:
            java_code: str = file.read()

            return (
                re.search(rf"public static .* {function_name}\(", java_code) is not None
            )

    except FileNotFoundError:
        return False


def validate_recursion_python(code: str, is_allowed_recursion: bool) -> dict:
    """
    Checks if a given Python code uses recursion.

    Args:
        code: The Python code to be tested.
        is_allowed_recursion: A boolean indicating whether recursion is allowed or not.

    Returns:
        A dictionary containing the result of the test and some feedback if the test fails.
    """
    if not is_allowed_recursion:
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
    code: str, is_allowed_recursion: bool, function_name: str
) -> dict:
    """
    Checks if a given Java code uses recursion.

    Args:
        code: The Java code to be tested.
        is_allowed_recursion: A boolean indicating whether recursion is allowed or not.
        function_name: The name of the function to be tested.

    Returns:
        A dictionary containing the result of the test and some feedback if the test fails.
    """
    if not is_allowed_recursion:
        matches = re.findall(function_name, code)

        if len(matches) > 3:
            return {
                "result": "Failure",
                "feedback": "La función no debe usar recursión.",
            }

    return {"result": "Success"}


def is_problem_function_working(
    problem: IProblem, user_submission: UserSubmission, user_code: dict | str
) -> dict:
    """
    Tests if a given function is working correctly.

    Args:
        problem: An IProblem instance containing the code to be tested and the language.
        user_submission: An UserSubmission instance containing the user's code and the language.
        user_code: The user's code to be tested. Could be a dictionary if the language is Python,
            or a string if the language is Java.

    Returns:
        A dictionary containing the result of the test in JSON format with the following keys:

        - result: str,  # Success/Failure
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output
    """
    try:
        all_expected_output: list = problem.get_expected_output()
        all_tested_output: list = problem.test_user_submission(
            user_code, user_submission
        )

        # Compare expected and tested outputs for all cases
        for i, (expected_output, tested_output) in enumerate(
            zip(all_expected_output, all_tested_output)
        ):
            if expected_output != tested_output:
                return {
                    "result": "Failure",
                    "expected_output": all_expected_output,
                    "tested_output": all_tested_output,
                    "feedback": f"Falló en el caso de prueba {i + 1}. " 
                        + "La función no retorna los valores esperados.",
                }

    except (TypeError, ValueError) as e:
        return {
            "result": "Failure",
            "expected_output": (
                all_expected_output if "all_expected_output" in locals() else None
            ),
            "tested_output": (
                all_tested_output if "all_tested_output" in locals() else None
            ),
            "feedback": f"Error de tipo en la función: {str(e)}",
        }

    except Exception as e:
        return {
            "result": "Failure",
            "expected_output": (
                all_expected_output if "all_expected_output" in locals() else None
            ),
            "tested_output": (
                all_tested_output if "all_tested_output" in locals() else None
            ),
            "feedback": f"Error en el código del usuario: {str(e)}",
        }

    # Return success if all test cases passed
    return {
        "result": "Success",
        "expected_output": all_expected_output,
        "tested_output": all_tested_output,
        "feedback": "La función retorna los valores esperados en todos los casos de prueba.",
    }


def execute_problem_python(problem: IProblem, user_submission: UserSubmission) -> dict:
    """
    Tests a Python problem.

    Args:
        problem: An IProblem instance containing the code to be tested and the language.

    Returns:
        A dictionary containing the result of the test in JSON format with the following keys:

        - result: str,  # Success/Failure
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output
    """
    code: str = user_submission.get_code()
    function_name: str = problem.get_python_function_name()
    local_vars: dict = {}

    # Execute code in local variables
    exec(code, {}, local_vars)

    # Check if function is defined
    if not is_problem_python_function_defined(local_vars, function_name):
        return {
            "result": "Failure",
            "feedback": f"Error: La función {function_name} no existe.",
        }

    # Check if function is working
    return is_problem_function_working(problem, user_submission, local_vars)


def test_problem_python(problem: IProblem, user_submission: UserSubmission) -> dict:
    """
    Tests a problem in Python.

    Args:
        problem: The problem to be tested.

    Returns:
        A dictionary containing the result of the test in JSON format with the following keys:

        - result: str,  # Success/Failure
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output
    """
    return execute_problem_python(problem, user_submission)


def compile_problem_java(
    problem: IProblem,
    user_submission: UserSubmission,
    function_name: str,
    temp_file_path: str,
) -> dict:
    """
    Compiles a Java problem and checks if the given function is defined and working.

    Args:
        problem: An IProblem instance containing the code to be tested and the language.
        user_submission: An UserSubmission instance containing the code to be tested.
        function_name: The expected name of the function to be tested.
        temp_file_path: The path to the temporary file where the code will be written.

    Returns:
        A dictionary containing the result of the test in JSON format with the following keys:

        - result: str,  # Success/Failure
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output
    """
    java_code: str = user_submission.get_code()

    # Write the code to a temp file
    with open(f"{temp_file_path}.java", "w", encoding="utf-8") as file:
        file.write(java_code)

    # Check if function is defined
    if not is_problem_java_function_defined(temp_file_path, function_name):
        return {
            "result": "Failure",
            "feedback": f"La función {function_name} no existe.",
        }

    # Compile the code
    compile_process = subprocess.run(
        ["javac", f"{temp_file_path}.java"], capture_output=True, check=True
    )

    # Check if compilation has failed
    if compile_process.returncode != 0:
        return {
            "result": "Failure",
            "feedback": compile_process.stderr.decode("utf-8"),
        }

    # Check if function is working
    return is_problem_function_working(problem, user_submission, temp_file_path)


def test_problem_java(problem: IProblem, user_submission: UserSubmission) -> dict:
    """
    Tests a problem in Java.

    Args:
        problem: The problem to be tested.
        user_submission: The user submission to be tested.

    Returns:
        A dictionary containing the result of the test in JSON format with the following keys:

        - result: str,  # Success/Failure
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output

    Raises:
        SyntaxError: If the code contains a syntax error.
        Exception: If any other error occurs during the test.

    Deletes the temp file and compiled class file after the test.
    """
    function_name: str = problem.get_java_function_name()
    temp_file_path: str = f"temp/{function_name}"

    result = compile_problem_java(
        problem, user_submission, function_name, temp_file_path
    )

    # Delete the temp file and compiled class file
    try:
        os.remove(f"{temp_file_path}.java")
        os.remove(f"{temp_file_path}.class")

    except FileNotFoundError:
        pass

    return result


def validate_metadata(problem: IProblem, user_submission: UserSubmission) -> dict:
    """
    Validates if the given code meets the requirements specified in the problem's metadata.

    Args:
        problem: An IProblem instance containing the code to be tested and the language.
        user_submission: An instance of UserSubmission containing the code to be tested.

    Returns:
        A dictionary containing the result of the test in JSON format with the following keys:

        - result: str,  # Success/Failure
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output
    """
    metadata: dict = problem.get_metadata()
    code: str = user_submission.get_code()
    language: str = user_submission.get_language()
    is_allowed_recursion: bool = metadata["allow_recursion"]
    disallowed_keywords: list = metadata["disallowed_keywords"]

    # Verify if the code contains disallowed keywords
    for keyword in disallowed_keywords:
        if keyword in code:
            return {
                "result": "Failure",
                "feedback": "El código contiene palabras no permitidas.",
            }

    # Verify if the code uses recursion
    if language == "python":
        return validate_recursion_python(code, is_allowed_recursion)

    if language == "java":
        function_name: str = problem.get_java_function_name()
        return validate_recursion_java(code, is_allowed_recursion, function_name)

    return {"result": "Failure", "feedback": "El lenguaje no es compatible."}


def jsonify_response(user_submission: UserSubmission, result_dict: dict) -> Response:
    """
    Creates a JSON response containing the result of a test.

    Args:
        user_submission: The user submission to be tested.
        result_dict: A dictionary containing the result of the test.

    Returns:
        A Flask Response object containing the JSON response.
    """

    problem_id: int = user_submission.get_problem_id()
    language: str = user_submission.get_language()

    # Create the response dictionary
    result: dict = {
        "problem_id": problem_id,
        "language": language,
    }

    # Add the result dictionary to the response dictionary
    result.update(result_dict)

    return jsonify(result)

def get_test_function_map() -> dict:
    """
    Returns a dictionary mapping the language name to the corresponding test function.

    Returns:
        dict: A dictionary mapping the language name to the corresponding test function.
    """
    return {
        'python': test_problem_python,
        'java': test_problem_java,
    }

def test_problem(problem: IProblem, user_submission: UserSubmission) -> tuple:
    """
    Tests a problem.

    Args:
        problem: The problem to be tested.
        user_submission: The user's submission to be tested.

    Returns:
        A tuple containing a JSON Response object and a status code.
        The JSON Response object contains the result of the test with the following keys:

        - result: str,  # Success/Failure
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output

        The status code is either 201 (Success) or 400 (Failure).
    """

    language: str = user_submission.get_language()
    test_function_map: dict = get_test_function_map()

    result_metadata: dict = validate_metadata(problem, user_submission)

    # Check if metadata validation has failed
    if result_metadata["result"] == "Failure":
        return jsonify_response(user_submission, result_metadata), 400

    # Evaluate test function
    result_dict: dict = test_function_map[language](problem, user_submission)

    # Return the jsonified response
    if result_dict["result"] == "Success":
        return jsonify_response(user_submission, result_dict), 201

    return jsonify_response(user_submission, result_dict), 400
