
from flask import jsonify, session
from app.problem_solver.interfaces.i_problem import IProblem
from app.problem_solver.problems.problem_1 import Problem1
from app.problem_solver.problems.problem_2 import Problem2
from app.problem_solver.problems.problem_3 import Problem3
from app.problem_solver.problems.problem_4 import Problem4
from app.problem_solver.problems.problem_5 import Problem5
from app.problem_solver.problems.problem_6 import Problem6
from app.problem_solver.problems.problem_7 import Problem7
from app.problem_solver.problems.problem_8 import Problem8
from app.problem_solver.problems.problem_9 import Problem9
from app.problem_solver.problems.problem_10 import Problem10
from app.problem_solver.models.user_submission import UserSubmission
from app.problem_solver.testing.code_tester import CodeTester


def get_problems_ids() -> list:
    """
    Returns a list of problem IDs as strings.

    Returns:
        list: A list of problem IDs as strings.
    """
    return list(str(key) for key in get_problems().keys())


def get_problems() -> dict:
    """
    Returns a dictionary of IProblem instances, each representing one problem.

    The dictionary keys are the problem IDs and the values are instances of the
    corresponding IProblem class.

    Returns:
        dict: A dictionary of IProblem instances.
    """
    return {1: Problem1(), 2: Problem2(), 3: Problem3(), 4: Problem4(), 5: Problem5(), 6: Problem6(), 7: Problem7(), 8: Problem8(), 9: Problem9(), 10: Problem10()}


def get_problem(problem_id: int) -> IProblem:
    """
    Returns an IProblem instance corresponding to the given problem ID.

    Args:
        problem_id (int): The ID of the problem to retrieve.

    Returns:
        IProblem: An instance of the IProblem class corresponding to the given problem ID.
    """
    problems_dict: dict = get_problems()

    return problems_dict[problem_id]


def get_number_of_problems() -> int:
    """
    Returns the number of problems in the system.

    Returns:
        int: The number of problems in the system.
    """
    return len(get_problems())


def run_code(problem_id: int, code: str, language: str, submit: bool = False) -> tuple:
    """
    Runs a given code for a given problem and language.

    Args:
        problem_id (int): The id of the problem to be tested.
        code (str): The code to be tested.
        language (str): The programming language of the code (python or java).

    Returns:
        A tuple containing a JSON response and a status code.

        The JSON response contains the result of the test in JSON format with the following keys:

        - result: str,  # Exito/Fallo
        - feedback: str,  # Feedback for the user
        - expected_output: list,  # Expected output
        - tested_output: list  # User's output

        The status code is either 200 (Success), 400 (Failure) or 404 (Problem not found or language not supported).

    Notes:
        This function assumes that the session has been initialized and contains the problem object.
        If any of the parameters is missing, it will return an error.
    """
    # Check if the session has been initialized and contains the problem object
    if "problem_object" not in session:
        return jsonify({"error": "Session no iniciada"}), 400

    if not problem_id or not language:
        return jsonify({"error": "Faltan datos"}), 400

    # Get the problem object
    problem_object: int = session["problem_object"]
    problem: IProblem = globals()[problem_object]()

    # Create a UserSubmission object
    submission = UserSubmission(problem_id, code, language)

    # Test the submission
    if problem_id in get_problems_ids():
        code_tester = CodeTester()
        return code_tester.test_problem(problem, submission, submit)

    return jsonify({"error": "Problema no encontrado o lenguaje no soportado."}), 400

def get_progress(user_progresses: list) -> list:
    progress_list = []

    for progress in user_progresses:
        progress_list.append(
            {
                "problem_id": progress.problem_id,
                "code": progress.code,
                "language": progress.language,
                "solved": progress.solved,
            }
        )

    return progress_list

def get_supported_languages() -> list[dict]:
    """
    Returns a list of supported languages with their respective metadata.
    """
    return [
        {"name": "Python", "value": "python", "mode": "python"},
        {"name": "Java", "value": "java", "mode": "text/x-java"},
        {"name": "Ruby", "value": "ruby", "mode": "text/x-ruby"},
    ]

def get_language_codes(problem: IProblem, last_codes=None) -> dict[str, dict[str, str]]:
    """
    Returns initial and last codes for all supported languages.
    """
    supported_languages = get_supported_languages()  
    last_codes = last_codes or {}

    codes = {}
    for lang in supported_languages:
        codes[lang["value"]] = {
            "initial": getattr(problem, f"get_initial_{lang['value']}_code")(),
            "last": last_codes.get(lang["value"], None)
        }
    return codes

