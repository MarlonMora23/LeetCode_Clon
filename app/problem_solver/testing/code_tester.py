from typing import Any, Dict
from flask import Response, jsonify
from app.problem_solver.handlers.java_handler import JavaHandler
from app.problem_solver.handlers.python_handler import PythonHandler
from app.problem_solver.handlers.strategies.multi_input_strategy import MultiInputStrategy
from app.problem_solver.handlers.strategies.single_input_strategy import SingleInputStrategy
from app.problem_solver.interfaces.i_base_test_strategy import IBaseTestStrategy
from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem
from app.problem_solver.models.user_submission import UserSubmission
from app.problem_solver.validators.code_validator import CodeValidator


class CodeTester:
    """Main class for handling code testing operations."""
    
    LANGUAGE_HANDLERS = {
        'python': PythonHandler,
        'java': JavaHandler
    }
    
    @classmethod
    def test_problem(cls, problem: 'IProblem', user_submission: 'UserSubmission') -> tuple[Response, int]:
        """Main method to test code submissions."""
        language: str = user_submission.get_language()
        code: str = user_submission.get_code()
        
        # Validate metadata requirements
        validator = CodeValidator(code, problem.get_metadata())
        keyword_result = validator.validate_keywords()
        
        if keyword_result:
            return cls._create_response(user_submission, keyword_result), 400
            
        recursion_result = validator.validate_recursion(
            language,
            problem.get_java_function_name() if language == "java" else ""
        )
        if recursion_result["result"] == "Fallo":
            return cls._create_response(user_submission, recursion_result), 400
        
        # Test the submission
        handler: ILanguageHandler = cls.LANGUAGE_HANDLERS[language](code)
        test_submission_result = handler.test_submission(problem)

        if test_submission_result["result"] == "Fallo":
            return cls._create_response(user_submission, test_submission_result), 400
        
        # Choose the strategy dynamically
        if hasattr(problem, "get_target"):
            strategy = MultiInputStrategy
        else:
            strategy = SingleInputStrategy

        result = cls.test_function(handler, problem, strategy)
        
        status_code = 201 if result["result"] == "Exito" else 400
        return cls._create_response(user_submission, result), status_code
    
    @staticmethod
    def test_function(handler: 'ILanguageHandler', problem: 'IProblem', strategy: 'IBaseTestStrategy') -> Dict[str, Any]:
        """Tests if a given function works correctly."""
        try:
            all_expected_output: list = problem.get_expected_output()
            all_tested_output: list = strategy.test(handler, problem)
            
            for i, (expected, tested) in enumerate(zip(all_expected_output, all_tested_output)):
                if expected != tested:
                    return {
                        "result": "Fallo",
                        "expected_output": all_expected_output,
                        "tested_output": all_tested_output,
                        "feedback": f"Falló en el caso de prueba {i + 1}. La función no retorna los valores esperados."
                    }
                    
            return {
                "result": "Exito",
                "expected_output": all_expected_output,
                "tested_output": all_tested_output,
                "feedback": "La función retorna los valores esperados en todos los casos de prueba."
            }
            
        except (TypeError, ValueError) as e:
            return {
                "result": "Fallo",
                "expected_output": locals().get('all_expected_output'),
                "tested_output": locals().get('all_tested_output'),
                "feedback": f"Error de tipo en la función: {str(e)}"
            }
        except Exception as e:
            return {
                "result": "Fallo",
                "expected_output": locals().get('all_expected_output'),
                "tested_output": locals().get('all_tested_output'),
                "feedback": f"Error en el código del usuario: {str(e)}"
            }
    
    @staticmethod
    def _create_response(user_submission: 'UserSubmission', result_dict: Dict[str, Any]) -> Response:
        """Creates a JSON response for the test results."""
        result = {
            "problem_id": user_submission.get_problem_id(),
            "language": user_submission.get_language(),
            **result_dict
        }
        return jsonify(result)