from app.problem_solver.interfaces.i_base_test_strategy import IBaseTestStrategy
from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem


class MultiInputStrategy(IBaseTestStrategy):
    @staticmethod
    def test(handler: "ILanguageHandler", problem: "IProblem") -> list:
        """Tests multi-input problems."""
        tested_output = []
        for target in problem.get_target():
            result = handler.execute(problem, problem.get_test_list(), target)
            tested_output.append(result)
        return tested_output
