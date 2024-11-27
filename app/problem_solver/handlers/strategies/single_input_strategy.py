from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem
from app.problem_solver.interfaces.i_base_test_strategy import IBaseTestStrategy 


class SingleInputStrategy(IBaseTestStrategy):
    @staticmethod
    def test(handler: "ILanguageHandler", problem: "IProblem") -> list:
        """Tests single-input problems."""
        tested_output = []
        try:
            for test_number in problem.get_test_list():
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

