from problem_solver.user_submission import UserSubmission
from problem_solver.i_problem import IProblem
import subprocess


def is_prime_number(n: int) -> bool:
    """
    Returns True if n is a prime number, False otherwise.
    A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.
    This function uses the square root optimization to check if a number is prime.
    Time complexity: O(sqrt(n))
    """
    if n <= 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


class Problem1(IProblem):
    def get_problem_id(self) -> int:
        return 1

    def get_test_list(self) -> list:
        return [3, 4, 7, 10, 11, 12, 19, 20, 23, 24, 29, 33, 37]

    def get_target(self) -> None:
        return None  # No target required for prime number check

    def get_expected_output(self) -> list:
        test_function: callable = self.get_test_function()

        return [test_function(i) for i in self.get_test_list()]

    def test_user_submission(
        self, user_code: dict | str, user_submission: UserSubmission
    ) -> list:
        tested_output: list = []
        if user_submission.language == "python":
            local_vars: dict = user_code
            user_function: callable = local_vars[self.get_python_function_name()]
            

            for test_number in self.get_test_list():
                tested_output.append(user_function(test_number))

            return tested_output

        if user_submission.language == "java":
            temp_file_path: str = user_code

            for test_number in self.get_test_list():
                run_process = subprocess.run(
                    ["java", temp_file_path, str(test_number)],
                    capture_output=True,
                    text=True,
                )

                java_result: str = run_process.stdout.strip()
                result: bool = java_result == "true"
                tested_output.append(result)

            return tested_output

    def get_python_function_name(self) -> str:
        return "is_prime_number"

    def get_java_function_name(self) -> str:
        return "isPrimeNumber"

    def get_test_function(self) -> callable:
        return is_prime_number

    def get_metadata(self) -> dict:
        return {"allow_recursion": False, "disallowed_keywords": ["while"]}

    def get_initial_python_code(self) -> str:
        return '''def is_prime_number(n: int) -> bool:
    """
    Checks if a given number is a prime number.

    Parameters  
    ----------
    n : int
        The number to be checked for primality.

    Returns
    -------
    bool
        True if the number is a prime number, False otherwise.
    """
    return None'''

    def get_initial_java_code(self) -> str:
        initial_code = """package temp;

public class isPrimeNumber {
    public static void main(String[] args) {      
        int n = Integer.parseInt(args[0]);        
        boolean result = isPrimeNumber(n);
        System.out.println(result);
    }

    public static boolean isPrimeNumber(int n) {
        // Your code goes here
        return false;
    }
}"""

        return initial_code
