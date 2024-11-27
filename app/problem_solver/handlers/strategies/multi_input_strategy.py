from app.problem_solver.interfaces.i_base_test_strategy import IBaseTestStrategy
from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem


class MultiInputStrategy(IBaseTestStrategy):
    @staticmethod
    def test(handler: "ILanguageHandler", problem: "IProblem") -> list:
        """Tests multi-input problems."""
        tested_output = []
        try:
            for target in problem.get_target():
                array_str = ','.join(map(str, problem.get_test_list()))
                result = handler.execute(problem, array_str, str(target))

                if problem.is_boolean():
                    if result == "true" or result == "True":
                        result = True
                    if result == "false" or result == "False":
                        result = False

                tested_output.append(result)
        finally:
            handler.cleanup_files()
        
        return tested_output
