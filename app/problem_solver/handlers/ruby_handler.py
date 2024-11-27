import os
import re
import subprocess
from typing import Any, Dict
from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem


class RubyHandler(ILanguageHandler):
    """Handles Ruby code testing and validation."""

    def __init__(self, code: str):
        self.code = code

    def is_function_defined(self, function_name: str) -> bool:
        """Checks if a function is defined in the Ruby code."""
        pattern = rf"def\s+{function_name}\b"
        return re.search(pattern, self.code) is not None
    
    def write_code(self, problem: "IProblem") -> None:
        with open(self.temp_file_path, "w", encoding="utf-8") as file:
            file.write(self.code)
            file.write("\n")
            file.write(problem.get_testing_ruby_code())

    def test_submission(self, problem: "IProblem") -> Dict[str, Any]:
        """Validates the Ruby code and checks for required functions."""
        function_name: str = problem.get_ruby_function_name()
        self.temp_file_path: str = f"app/temp/{function_name}.rb"

        if not self.is_function_defined(function_name):
            return {
                "result": "Fallo",
                "feedback": f"La función {function_name} no está definida en el código.",
            }

        # Save the user code to a temporary Ruby file
        try:
            self.write_code(problem)

        except IOError as e:
            return {
                "result": "Fallo",
                "feedback": f"Error al guardar el archivo temporal: {str(e)}",
            }

        return {"result": "Exito"}

    def execute(self, problem: "IProblem", *inputs) -> Any:
        """Executes the user code for Ruby with the given inputs."""
        try:
            # Prepare the command to execute the Ruby script with arguments
            ruby_params = [str(i) for i in inputs]
            run_process = subprocess.run(
                ["ruby", self.temp_file_path] + ruby_params,
                capture_output=True,
                text=True,
                check=True,
            )
            return run_process.stdout.strip()  # Ruby output as a string
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ruby execution failed: {e.stderr}")

    def cleanup_files(self) -> None:
        """Removes temporary files created for Ruby execution."""
        try:
            os.remove(self.temp_file_path)
        except FileNotFoundError:
            pass
