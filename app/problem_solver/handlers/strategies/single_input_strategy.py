from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem
from app.problem_solver.interfaces.i_base_test_strategy import IBaseTestStrategy 


class SingleInputStrategy(IBaseTestStrategy):
    @staticmethod
    def test(handler: "ILanguageHandler", problem: "IProblem") -> list:
        """Tests single-input problems."""
        tested_output = []
        for test_number in problem.get_test_list():
            result = handler.execute(problem, test_number)
            tested_output.append(result)
        return tested_output
