import subprocess
import os
from flask import Response, jsonify
from problems.MyApp import (
    is_problem_python_function_defined,
    is_problem_java_function_defined,
    validate_metadata,
    get_metadata,
)


def is_prime_number(n: int) -> bool:
    """
    Returns True if n is a prime number, False otherwise.
    A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.
    This function uses the square root optimization to check if a number is prime.
    Time complexity: O(sqrt(n))
    """
    if n <= 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


def is_problem_1_python_function_working(
    local_vars: dict, expected_function_name: str, test_list: list[int]
) -> dict:
    """
    Tests if the specified Python function in `local_vars` works correctly.

    Args:
        local_vars: A dictionary containing the local variables of the function's scope.
        expected_function_name: The expected name of the function to be tested.
        test_list: A list of test values to be passed to the function.

    Returns:
        A dictionary containing the test results, including success status, expected and tested outputs, and feedback.
    """

    expected_output: list[bool] = [
        is_prime_number(test_number) for test_number in test_list
    ]
    tested_output: list[bool] = []

    try:
        for test_number in test_list:
            result: bool = local_vars[expected_function_name](test_number)
            tested_output.append(result)

        if expected_output != tested_output:
            return {
                "result": "Failure",
                "expected_output": expected_output,
                "tested_output": tested_output,
                "feedback": "La función no retorna los valores esperados.",
            }

    except (TypeError, ValueError) as e:
        return {
            "result": "Failure",
            "expected_output": expected_output,
            "tested_output": tested_output,
            "feedback": f"Error en la función {expected_function_name}: {str(e)}",
        }

    except Exception as e:
        return {
            "result": "Failure",
            "expected_output": expected_output,
            "tested_output": tested_output,
            "feedback": f"Error inesperado en la función {expected_function_name}: {str(e)}",
        }

    return {
        "result": "Success",
        "expected_output": expected_output,
        "tested_output": tested_output,
        "feedback": "La funcion retorna los valores esperados.",
    }


def is_problem_1_java_function_working(
    expected_function_name: str, test_list: list[int], temp_file_path: str
) -> dict:
    """
    Tests if the specified Java function in a temp file works correctly.

    Args:
        expected_function_name: The expected name of the function to be tested.
        test_list: A list of test values to be passed to the function.
        temp_file_path: The path to the temp file containing the Java code.

    Returns:
        A dictionary containing the test results, including success status, expected and tested outputs, and feedback.
    """

    expected_output: list[bool] = [
        is_prime_number(test_number) for test_number in test_list
    ]
    tested_output: list[bool] = []

    try:
        for test_number in test_list:

            # Execute the code
            run_process = subprocess.run(
                ["java", temp_file_path, str(test_number)],
                capture_output=True,
                text=True,
            )
            result: str = run_process.stdout.strip()
            tested_output.append(result == "true")

        if expected_output != tested_output:
            return {
                "result": "Failure",
                "expected_output": expected_output,
                "tested_output": tested_output,
                "feedback": "La función no retorna los valores esperados.",
            }

    except (TypeError, ValueError) as e:
        return {
            "result": "Failure",
            "expected_output": expected_output,
            "tested_output": tested_output,
            "feedback": f"Error de tipoen la función {expected_function_name}: {str(e)}",
        }

    except Exception as e:
        return {
            "result": "Failure",
            "expected_output": expected_output,
            "tested_output": tested_output,
            "feedback": f"Error inesperado en la función {expected_function_name}: {str(e)}",
        }

    return {
        "result": "Success",
        "expected_output": expected_output,
        "tested_output": tested_output,
        "feedback": "La funcion retorna los valores esperados.",
    }


def test_problem_1_python(
    code: str, expected_function_name: str, test_list: list[int]
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
    result_dict: dict = is_problem_1_python_function_working(
        local_vars, expected_function_name, test_list
    )

    return result_dict


def test_problem_1_java(
    code: str, expected_function_name: str, test_list: list[int]
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
    temp_file_path: str = "temp/PrimeCheck"

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
        result_dict: dict = is_problem_1_java_function_working(
            expected_function_name, test_list, temp_file_path
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
    expected_function_name: str,
    test_list: list[int],
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

    test_function: str = f"test_problem_{problem_id}_{language}"
    result_dict: dict = eval(test_function)(
        data["code"], expected_function_name, test_list
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


def test_problem_1(data: dict) -> tuple:
    """
    Tests problem 1 in the given language.

    Args:
        data: A dictionary containing the code to be tested and the language.

    Returns:
        A tuple containing the result of the test in JSON format and a status code.
    """
    test_list: list[int] = [3, 4, 7, 10, 11, 12, 19, 20, 23, 24, 29, 33, 37]
    metadata = get_metadata()

    if data["language"] == "python":
        expected_function_name: str = "is_prime_number"

        return test_problem_in(
            language="python",
            problem_id=1,
            data=data,
            expected_function_name=expected_function_name,
            test_list=test_list,
            metadata=metadata,
        )

    elif data["language"] == "java":
        expected_function_name: str = "isPrimeNumber"

        return test_problem_in(
            language="java",
            problem_id=1,
            data=data,
            expected_function_name=expected_function_name,
            test_list=test_list,
            metadata=metadata,
        )
