import os
import re
import subprocess
from typing import Any, Dict
from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem


class JavaHandler(ILanguageHandler):
    """Handles Java code testing and validation."""

    def __init__(self, code: str):
        self.code = code

    def is_function_defined(self, function_name: str) -> bool:
        return re.search(rf"public static .* {function_name}\(", self.code) is not None

    def test_submission(self, problem: "IProblem") -> Dict[str, Any]:
        function_name: str = problem.get_java_function_name()
        self.temp_file_path: str = f"app/temp/{function_name}"

        try:
            return self._compile_and_test(function_name)

        except subprocess.CalledProcessError as e:
            self._cleanup_files()
            return {"result": "Fallo", "feedback": [str(e.stderr)]}

    def _compile_and_test(
        self,
        function_name: str,
    ) -> Dict[str, Any]:
        with open(f"{self.temp_file_path}.java", "w", encoding="utf-8") as file:
            file.write(self.code)

        if not self.is_function_defined(function_name):
            return {
                "result": "Fallo",
                "feedback": f"La función {function_name} no existe.",
            }

        compile_process = subprocess.run(
            ["javac", f"{self.temp_file_path}.java"], capture_output=True, check=True
        )

        if compile_process.returncode != 0:
            return {
                "result": "Fallo",
                "feedback": compile_process.stderr.decode("utf-8"),
            }

        return {"result": "Exito"}

    def _cleanup_files(self) -> None:
        try:
            os.remove(f"{self.temp_file_path}.java")
            os.remove(f"{self.temp_file_path}.class")

        except FileNotFoundError:
            pass

    def execute(self, problem: "IProblem", *inputs) -> Any:
        """Executes the user code for Java with the given inputs."""
        try:
            # Convert inputs to strings to pass as command-line arguments
            java_params = [str(i) for i in inputs]
            run_process = subprocess.run(
                ["java", self.temp_file_path] + java_params,
                capture_output=True,
                text=True,
                check=True,
            )
            return run_process.stdout.strip()  # Java output as a string
        except subprocess.CalledProcessError as e:
            self._cleanup_files()
            raise RuntimeError(f"Java execution failed: {e.stderr}")
