from typing import Any, Dict
from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem


class PythonHandler(ILanguageHandler):
    """Handles Python code testing and validation."""

    def __init__(self, code: str):
        self.code = code
        self.local_vars: Dict[str, Any] = {}

    def is_function_defined(self, function_name: str) -> bool:
        exec(self.code, {}, self.local_vars)
        return function_name in self.local_vars

    def test_submission(self, problem: "IProblem") -> Dict[str, Any]:
        function_name: str = problem.get_python_function_name()

        if not self.is_function_defined(function_name):
            return {
                "result": "Fallo",
                "feedback": f"Error: La función {function_name} no existe.",
            }

        return {"result": "Exito"}

    def execute(self, problem: "IProblem", *inputs) -> Any:
        """Executes the user code for Python with the given inputs."""
        user_function = self.local_vars[problem.get_python_function_name()]
        return user_function(*inputs)
