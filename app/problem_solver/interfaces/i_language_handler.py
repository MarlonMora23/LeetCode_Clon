from abc import ABC, abstractmethod
from typing import Dict, Any
from contextlib import contextmanager
from app.problem_solver.interfaces.i_problem import IProblem


class ILanguageHandler(ABC):
    """Abstract base class for language-specific code handling."""

    @abstractmethod
    def is_function_defined(self, function_name: str) -> bool:
        pass

    @abstractmethod
    def test_submission(self, problem: "IProblem") -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute(self, problem: "IProblem", *inputs) -> Any:
        pass

    @abstractmethod
    def cleanup_files(self) -> None:
        """Optional: Removes temporary files created during execution."""
        pass  # Empty for languages without temporary files
