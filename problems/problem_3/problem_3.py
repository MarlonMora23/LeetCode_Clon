from flask import jsonify

from problems.MyApp import test_problem, get_metadata, validate_metadata
import random

def is_problem_3_python_function_working(local_vars: dict, test_list: list[int]) -> dict:
    """
    Tests if the specified Python function in local_vars works correctly for problem 3.

    Args:
        local_vars: A dictionary containing the local variables of the function's scope.
        test_list: A list of test values to be passed to the function.

    Returns:
        A dictionary containing the test results, including success status, expected and tested outputs, and feedback.
    """
    try:
        generator_instance = local_vars["Generator"]()

        numbers_in_array, numbers_not_in_array = generator_instance.search_number()

        expected_in_array = [random.choice(array) for array in generator_instance.arrays_sum]
        expected_not_in_array = []
        for array in generator_instance.arrays_sum:
            number_not_in = random.randint(0, 100)
            while number_not_in in array:
                number_not_in = random.randint(0, 100)
            expected_not_in_array.append(number_not_in)

        if numbers_in_array == expected_in_array and numbers_not_in_array == expected_not_in_array:
            return {
                "result": "Success",
                "expected_numbers_in_array": expected_in_array,
                "tested_numbers_in_array": numbers_in_array,
                "expected_numbers_not_in_array": expected_not_in_array,
                "tested_numbers_not_in_array": numbers_not_in_array,
                "feedback": "La función retorna los valores esperados."
            }
        else:
            return {
                "result": "Failure",
                "expected_numbers_in_array": expected_in_array,
                "tested_numbers_in_array": numbers_in_array,
                "expected_numbers_not_in_array": expected_not_in_array,
                "tested_numbers_not_in_array": numbers_not_in_array,
                "feedback": "La función no retorna los valores esperados."
            }

    except Exception as e:
        return {
            "result": "Failure",
            "feedback": f"Error inesperado en la función: {str(e)}"
        }


def test_problem_3(data: dict) -> tuple:
    """
    Tests problem 3 in the given language.

    Args:
        data: A dictionary containing the code to be tested and the language.

    Returns:
        A tuple containing the result of the test in JSON format and a status code.
    """
    test_list: list[int] = [2, 3, 23, 24, 34, 55, 59, 60, 70, 73]
    metadata = get_metadata()

    
    result_metadata = validate_metadata(
        code=data["code"],
        metadata=metadata,
        problem_number=3,
        language=data["language"],
        required_class="Generator"
    )

    if result_metadata["result"] == "Failure":
        return jsonify(result_metadata), 400

    if data["language"] == "python":
       
        result_dict = test_problem(
            data=data,
            test_list=test_list,
            problem_id=3,
            test_function=is_problem_3_python_function_working,
            python_func_name="Generator",
            java_func_name="Generator"
        )

        if result_dict["result"] == "Success":
            return jsonify(result_dict), 201
        else:
            return jsonify(result_dict), 400

    return jsonify({"error": "Language not supported"}), 400