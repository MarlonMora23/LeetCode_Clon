from abc import ABC, abstractmethod

from app.problem_solver.interfaces.i_language_handler import ILanguageHandler
from app.problem_solver.interfaces.i_problem import IProblem


class IBaseTestStrategy(ABC):
    """Base class for all test strategies."""

    @abstractmethod
    def test(handler: ILanguageHandler, problem: IProblem) -> list:
        """
        Executes the testing logic for a given handler and problem.
        Must be implemented by concrete strategies.
        """
        pass
