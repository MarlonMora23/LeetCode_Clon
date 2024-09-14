from abc import ABC, abstractmethod
from problem_solver.user_submission import UserSubmission

class IProblem(ABC):
    @abstractmethod
    def get_problem_id(self) -> int:
        pass

    @abstractmethod
    def get_test_list(self) -> list:
        pass

    @abstractmethod
    def get_expected_output(self) -> list:
        pass

    @abstractmethod
    def test_user_submission(self, user_code: dict | str, user_submission: UserSubmission) -> list:
        pass

    @abstractmethod
    def get_target(self) -> any:
        pass

    @abstractmethod
    def get_python_function_name(self) -> str:
        pass

    @abstractmethod
    def get_java_function_name(self) -> str:
        pass

    @abstractmethod
    def get_test_function(self) -> callable:
        pass

    @abstractmethod
    def get_metadata(self) -> dict:
        pass

    @abstractmethod
    def get_initial_python_code(self) -> str:
        pass
    
    @abstractmethod
    def get_initial_java_code(self) -> str:
        pass
