class UserSubmission:
    def __init__(self, problem_id: int, code: str, language: str):
        self.problem_id: int = problem_id
        self.code: str = code
        self.language: str = language

    def get_problem_id(self) -> int:
        return self.problem_id

    def get_code(self) -> str:
        return self.code

    def get_language(self) -> str:
        return self.language