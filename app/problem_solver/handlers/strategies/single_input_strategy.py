from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem
from app.problem_solver.interfaces.i_base_test_strategy import IBaseTestStrategy 


class SingleInputStrategy(IBaseTestStrategy):
    @staticmethod
    def test(handler: "ILanguageHandler", problem: "IProblem", submit: bool) -> list:
        """Tests single-input problems."""
        tested_output = []
        test_list = problem.get_test_list() if not submit else problem.get_submission_test_list()
        try:
            for test_number in test_list:
                if type(test_number) is str or type(test_number) is int or type(test_number) is float:
                    result = handler.execute(problem, test_number)

                if type(test_number) is list:
                    if handler.__class__.__name__ == "JavaHandler":
                        result = handler.execute(problem, *test_number)

                    if handler.__class__.__name__ == "PythonHandler":
                        result = handler.execute(problem, test_number)

                    if handler.__class__.__name__ == "RubyHandler":
                        result = handler.execute(problem, test_number)

                if problem.is_boolean():
                    if result == "true" or result == "True":
                        result = True
                    if result == "false" or result == "False":
                        result = False

                if result == "":
                    result = None

                if result == "null":
                    result = None

                if problem.is_integer():
                    if result is not None:
                        result = int(result)

                tested_output.append(result)
        finally:
            handler.cleanup_files()  

        return tested_output

