"""
This module contains some abstracted functions to test Python and Java code.
"""

import ast
import os
import re
import subprocess

from flask import Response, jsonify

from problems.i_problem import IProblem


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

        if len(matches) > 3:
            return {
                "result": "Failure",
                "feedback": "La función no debe usar recursión.",
            }

        return {"result": "Success"}

    return {"result": "Success"}


def is_problem_python_function_working(
    local_vars: dict,
    expected_function_name: str,
    test_list: list[int],
    test_function: callable,
    targets: list[any] = None,
    n_test_cases: int = 1,
) -> dict:
    """
    Tests if the specified Python function in `local_vars` works correctly.

    Args:
        local_vars: A dictionary containing the local variables of the function's scope.
        expected_function_name: The expected name of the function to be tested.
        test_list: A list of test values to be passed to the function.
        targets: An optional list of parameters (like target values) to be passed to the function if required.
        n_test_cases: Number of test cases to be executed.

    Returns:
        A dictionary containing the test results, including success status, expected and tested outputs, and feedback.
    """

    # Make sure the number of test cases matches the provided target list (if targets are provided)
    if targets is None:
        targets = [None] * n_test_cases  # If no targets are provided, set them to None

    if len(targets) != n_test_cases:
        return {
            "result": "Failure",
            "feedback": "El número de objetivos (targets) no coincide con el número de casos de prueba.",
        }

    # Initialize results
    all_expected_output = []
    all_tested_output = []

    try:
        # Loop through each test case
        for i in range(n_test_cases):
            target = targets[i]

            # Determine the expected output for the current test case
            if target is not None:
                expected_output = [
                    test_function(test_number, target) for test_number in test_list
                ]

            else:
                expected_output = [
                    test_function(test_number) for test_number in test_list
                ]

            all_expected_output.append(expected_output)

            # Test the user's function with the provided target
            tested_output = []
            for test_number in test_list:
                if target is not None:
                    result = local_vars[expected_function_name](test_number, target)
                else:
                    result = local_vars[expected_function_name](test_number)
                tested_output.append(result)

            all_tested_output.append(tested_output)

        # Compare the expected output with the tested output for all test cases
        for i in range(n_test_cases):
            if all_expected_output[i] != all_tested_output[i]:
                return {
                    "result": "Failure",
                    "expected_output": all_expected_output,
                    "tested_output": all_tested_output,
                    "feedback": f"Falló en el caso de prueba {i + 1}. La función no retorna los valores esperados.",
                }

    except (TypeError, ValueError) as e:
        return {
            "result": "Failure",
            "expected_output": all_expected_output,
            "tested_output": all_tested_output,
            "feedback": f"Error en la función {expected_function_name}: {str(e)}",
        }

    except Exception as e:
        return {
            "result": "Failure",
            "expected_output": all_expected_output,
            "tested_output": all_tested_output,
            "feedback": f"Error inesperado en la función {expected_function_name}: {str(e)}",
        }

    # Return success if all test cases passed
    return {
        "result": "Success",
        "expected_output": all_expected_output,
        "tested_output": all_tested_output,
        "feedback": "La función retorna los valores esperados en todos los casos de prueba.",
    }


def is_problem_java_function_working(
    expected_function_name: str,
    test_list: list[int],
    test_function: callable,
    temp_file_path: str,
    targets: list[any] = None,
    n_test_cases: int = 1,
) -> dict:
    """
    Tests if the specified Java function in a temp file works correctly.

    Args:
        expected_function_name: The expected name of the function to be tested.
        test_list: A list of test values to be passed to the function.
        temp_file_path: The path to the temp file containing the Java code.
        targets: An optional list of target values to pass to the function for each test case.
        n_test_cases: Number of test cases to execute.

    Returns:
        A dictionary containing the test results, including success status, expected and tested outputs, and feedback.
    """

    # Ensure targets list is valid
    if targets is None:
        targets = [None] * n_test_cases  # If no targets are provided, set them to None

    if len(targets) != n_test_cases:
        return {
            "result": "Failure",
            "feedback": "El número de objetivos (targets) no coincide con el número de casos de prueba.",
        }

    all_expected_output = []
    all_tested_output = []

    try:
        for i in range(n_test_cases):
            target = targets[i]

            # Determine the expected output for the current test case
            if target is not None:
                expected_output = [
                    test_function(test_number, target) for test_number in test_list
                ]
            else:
                expected_output = [
                    test_function(test_number) for test_number in test_list
                ]

            all_expected_output.append(expected_output)

            tested_output = []

            # Execute the user's Java function for each test number in the test list
            for test_number in test_list:
                # Prepare the command for running the Java file, passing the test_number and target if applicable
                if target is not None:
                    run_process = subprocess.run(
                        ["java", temp_file_path, str(test_number), str(target)],
                        capture_output=True,
                        text=True,
                    )
                else:
                    run_process = subprocess.run(
                        ["java", temp_file_path, str(test_number)],
                        capture_output=True,
                        text=True,
                    )

                result: str = run_process.stdout.strip()
                tested_output.append(result == "true")

            all_tested_output.append(tested_output)

        # Compare expected and tested outputs for all cases
        for i in range(n_test_cases):
            if all_expected_output[i] != all_tested_output[i]:
                return {
                    "result": "Failure",
                    "expected_output": all_expected_output,
                    "tested_output": all_tested_output,
                    "feedback": f"Falló en el caso de prueba {i + 1}. La función no retorna los valores esperados.",
                }

    except (TypeError, ValueError) as e:
        return {
            "result": "Failure",
            "expected_output": all_expected_output,
            "tested_output": all_tested_output,
            "feedback": f"Error de tipo en la función {expected_function_name}: {str(e)}",
        }

    except Exception as e:
        return {
            "result": "Failure",
            "expected_output": all_expected_output,
            "tested_output": all_tested_output,
            "feedback": f"Error inesperado en la función {expected_function_name}: {str(e)}",
        }

    # Return success if all test cases passed
    return {
        "result": "Success",
        "expected_output": all_expected_output,
        "tested_output": all_tested_output,
        "feedback": "La función retorna los valores esperados en todos los casos de prueba.",
    }


def test_problem_python(
    code: str,
    expected_function_name: str,
    test_list: list[int],
    test_function: callable,
    target: any = None,
    n_test_cases: int = 1,
) -> dict:
    """
    Tests a problem given the code, expected function name, and test list.

    Args:
        code: The code to be tested.
        expected_function_name: The expected name of the function in the code.
        test_list: A list of test values to be passed to the function.

    Returns:
        A dictionary containing the test results, including success status, expected and tested outputs, and feedback.
    """
    try:
        local_vars: dict = {}

        # Execute code in local variables
        exec(code, {}, local_vars)

    except SyntaxError as e:
        return {
            "result": "Failure",
            "feedback": f"Error: Error de sintaxis: {str(e)}",
        }

    except Exception as e:
        return {
            "result": "Failure",
            "feedback": f"Error: Error inesperado: {str(e)}",
        }

    # Check if function is defined
    if not is_problem_python_function_defined(local_vars, expected_function_name):
        return {
            "result": "Failure",
            "feedback": f"Error: La función {expected_function_name} no existe.",
        }

    # Check if function is working
    result_dict: dict = is_problem_python_function_working(
        local_vars,
        expected_function_name,
        test_list,
        test_function,
        target,
        n_test_cases,
    )

    return result_dict


def test_problem_java(
    code: str,
    expected_function_name: str,
    test_list: list[int],
    test_function: callable,
    target: any = None,
    n_test_cases: int = 1,
) -> dict:
    """
    Tests if the specified Java function in `code` works correctly.

    Args:
        code: The Java code containing the function to be tested.
        expected_function_name: The expected name of the function to be tested.
        test_list: A list of test values to be passed to the function.

    Returns:
        A dictionary containing the test results, including success status, expected and tested outputs, and feedback.
    """
    temp_file_path: str = f"temp/{expected_function_name}"

    try:
        # Write the code to a temp file
        with open(f"{temp_file_path}.java", "w") as file:
            file.write(code)

        # Check if function is defined
        if not is_problem_java_function_defined(temp_file_path, expected_function_name):
            return {
                "result": "Failure",
                "feedback": f"Error: La función {expected_function_name} no existe.",
            }

        # Compile the code
        compile_process = subprocess.run(
            ["javac", f"{temp_file_path}.java"], capture_output=True
        )

        if compile_process.returncode != 0:
            return {
                "result": "Failure",
                "feedback": compile_process.stderr.decode("utf-8"),
            }

        # Check if function is working
        result_dict: dict = is_problem_java_function_working(
            expected_function_name,
            test_list,
            test_function,
            temp_file_path,
            target,
            n_test_cases,
        )

        return result_dict

    except SyntaxError as e:
        return {
            "result": "Failure",
            "feedback": f"Error: Error de sintaxis: {str(e)}",
        }

    except Exception as e:
        return {
            "result": "Failure",
            "feedback": f"Error: Error inesperado: {str(e)}",
        }

    finally:
        # Delete the temp file and compiled class file
        try:
            os.remove(f"{temp_file_path}.java")
            os.remove(f"{temp_file_path}.class")

        except FileNotFoundError:
            pass


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


def jsonify_response(problem_id: int, language: str, result_dict: dict) -> Response:
    """
    Returns a JSON response with the given problem_id, language, result, expected_output, tested_output and feedback.

    Args:
        problem_id: The id of the problem.
        language: The language of the submission.
        result_dict: A dictionary containing the result of the submission.

    Returns:
        A JSON response with the given problem_id, language, result, expected_output, tested_output and feedback.
    """
    result: dict = {
        "problem_id": problem_id,
        "language": language,
    }

    result.update(result_dict)

    return jsonify(result)


def test_problem_in(
    language: str,
    problem_id: int,
    data: dict,
    test_function: callable,
    expected_function_name: str,
    test_list: list,
    target: any,
    n_test_cases: int,
    metadata: dict,
) -> tuple:
    """
    Tests a problem given the language, problem ID, code, expected function name, and test list.

    Args:
        language: The language of the code.
        problem_id: The ID of the problem.
        data: A dictionary containing the code and other information.
        expected_function_name: The expected name of the function in the code.
        test_list: A list of test values to be passed to the function.
        metadata: A dictionary containing metadata about the problem.

    Returns:
        A tuple containing a JSON response and a status code.
    """
    result_metadata = validate_metadata(
        data["code"], metadata, problem_id, language, expected_function_name
    )

    if result_metadata["result"] == "Failure":
        return (
            jsonify_response(problem_id, language, result_metadata),
            400,
        )

    test_function_name: str = f"test_problem_{language}"
    result_dict: dict = eval(test_function_name)(
        data["code"],
        expected_function_name,
        test_list,
        test_function,
        target,
        n_test_cases,
    )

    if result_dict["result"] == "Success":
        return (
            jsonify_response(problem_id, language, result_dict),
            201,
        )

    if result_dict["result"] == "Failure":
        return (
            jsonify_response(problem_id, language, result_dict),
            400,
        )


def get_metadata() -> dict:
    """
    Returns a dictionary containing metadata about the problems.

    The dictionary maps problem IDs to another dictionary containing two keys:

    - "allow_recursion": A boolean indicating whether recursion is allowed in the solution.
    - "disallowed_keywords": A list of keywords that should not be used in the solution.

    """
    return {
        1: {"allow_recursion": False, "disallowed_keywords": ["while"]},
        2: {"allow_recursion": False, "disallowed_keywords": ["while"]},
        3: {"allow_recursion": False, "disallowed_keywords": ["while"]},
    }


def test_problem(problem: IProblem, data: dict) -> dict:
    """
    Tests a problem using the provided problem instance.

    Args:
        problem: An instance of IProblem implementing the specific test case.
        data: A dictionary containing the code to be tested and the language.
        problem_id: The ID of the problem.

    Returns:
        A tuple containing the result of the test in JSON format and a status code.
    """
    metadata = get_metadata()

    if data["language"] == "python":
        expected_function_name = problem.get_python_function_name()
    elif data["language"] == "java":
        expected_function_name = problem.get_java_function_name()

    return test_problem_in(
        language=data["language"],
        problem_id=problem.get_problem_id(),
        data=data,
        test_function=problem.get_test_function(),
        expected_function_name=expected_function_name,
        test_list=problem.get_test_list(),
        target=problem.get_target(),
        n_test_cases=problem.get_n_test_cases(),
        metadata=metadata,
    )
