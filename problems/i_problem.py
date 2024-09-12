from abc import ABC, abstractmethod

class IProblem(ABC):
    @abstractmethod
    def get_problem_id(self) -> int:
        pass

    @abstractmethod
    def get_test_list(self) -> list:
        pass

    @abstractmethod
    def get_target(self) -> any:
        pass

    @abstractmethod
    def get_n_test_cases(self) -> int:
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
