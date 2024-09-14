import re
import subprocess
from problem_solver.user_submission import UserSubmission
from problem_solver.i_problem import IProblem


def validate_password(password: str) -> bool:
    """
    Validates if a given password meets the requirements specified in the problem's metadata.

    Args:
        password: The password to be tested.

    Returns:
        A boolean indicating whether the password is valid or not.
    """
    # At least 8 characters
    if len(password) < 8:
        return False

    # At least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # At least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False

    # At least one digit
    if not re.search(r"\d", password):
        return False

    # At least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


class Problem2(IProblem):
    def get_problem_id(self) -> int:
        return 2

    def get_test_list(self) -> list[str]:
        return [
            # Valid passwords
            "Password1!",
            "Valid123$",
            "Str0ngP@ssw0rd",
            # Invalid passwords
            "short1!",  # Less than 8 characters
            "nouppercase1!",  # No uppercase letters
            "NOLOWERCASE1!",  # No lowercase letters
            "NoSpecial123",  # No special characters
            "NoDigits!",  # No numbers
            "",  # Empty password
            "12345678",  # Only numbers, no letters or special characters
            "abcdefgh",  # Only lowercase letters, no numbers or special characters
            "ABCDEFGH",  # Only uppercase letters, no numbers or special characters
            "!@#$%^&*()",
        ]

    def get_target(self) -> any:
        return None  # No target required for password validation

    def get_expected_output(self) -> list:
        test_function: callable = self.get_test_function()

        return [test_function(password) for password in self.get_test_list()]

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
        return "validate_password"

    def get_java_function_name(self) -> str:
        return "validatePassword"

    def get_test_function(self) -> callable:
        return validate_password

    def get_metadata(self) -> dict:
        return {"allow_recursion": False, "disallowed_keywords": ["while"]}

    def get_initial_python_code(self) -> str:
        return '''def validate_password(password: str) -> bool:
    """
    Validates if a given password meets the requirements specified in the problem's metadata.

    Args:
        password: The password to be tested.

    Returns:
        A boolean indicating whether the password is valid or not.
    """
    return None'''

    def get_initial_java_code(self) -> str:
        return """package temp;

public class validatePassword {
    public static void main(String[] args) {      
        String n = String.valueOf(args[0]);        
        boolean result = validatePassword(n);
        System.out.println(result);
    }

    public static boolean validatePassword(String n) {
        // Your code goes here
        return false;
    }
}"""
