import random
import subprocess
from problem_solver.user_submission import UserSubmission
from problem_solver.i_problem import IProblem


def search_number(array: list, target: int):
    """
    Searches for a target in an array and returns True if found, False otherwise

    Parameters
    ----------
    array : list
        The array to search in
    target : int
        The target to search for

    Returns
    -------
    bool
        True if the target is found in the array, False otherwise
    """
    return target in array


def targets_matches_test_cases(targets: list[int], test_cases: list[list[int]]) -> bool:
    """
    Checks if the targets match the test cases.

    Parameters
    ----------
    targets : List[int]
        The targets to check
    test_cases : List[List[int]]
        The test cases to check against

    Returns
    -------
    bool
        True if the targets match the test cases, False otherwise
    """
    if len(targets) != len(test_cases):
        return False

    for i in range(len(targets)):
        if targets[i] != test_cases[i]:
            return False

    return True


class Problem3(IProblem):
    def get_problem_id(self) -> int:
        return 3

    def get_test_list(self) -> list:
        return [3, 4, 7, 10, 11, 12, 19, 20, 23, 24, 29, 33, 37]

    def get_target(self) -> any:
        return [3, 5, 12, 22, 37]

    def get_expected_output(self) -> list:
        test_function: callable = self.get_test_function()

        return [
            test_function(self.get_test_list(), target) for target in self.get_target()
        ]

    def test_user_submission(
        self, user_code: dict | str, user_submission: UserSubmission
    ) -> list:
        tested_output: list = []
        test_list: list = self.get_test_list()

        if user_submission.language == "python":
            local_vars: dict = user_code
            user_function: callable = local_vars[self.get_python_function_name()]
            

            for target in self.get_target():
                tested_output.append(user_function(test_list, target))

            return tested_output

        if user_submission.language == "java":
            temp_file_path: str = user_code

            for target in self.get_target():
                java_params: list = [str(i) for i in test_list] + [str(target)]
                run_process = subprocess.run(
                    ["java", temp_file_path] + java_params,  
                    capture_output=True,
                    text=True,
                )

                java_result: str = run_process.stdout.strip()
                result = java_result == "true"
                tested_output.append(result)

            return tested_output


    def get_python_function_name(self) -> str:
        return "search_number"

    def get_java_function_name(self) -> str:
        return "searchNumber"

    def get_test_function(self) -> callable:
        return search_number

    def get_metadata(self) -> dict:
        return {"allow_recursion": False, "disallowed_keywords": ["while"]}

    def get_initial_python_code(self) -> str:
        return '''def search_number(array: list, target: int):
    """
    Searches for a target in an array and returns True if found, False otherwise
    
    Parameters
    ----------
    array : list
        The array to search in
    target : int
        The target to search for
    
    Returns
    -------
    bool
        True if the target is found in the array, False otherwise
    """
    return None'''

    def get_initial_java_code(self) -> str:
        return """package temp;

public class searchNumber {
    public static void main(String[] args) {
        int[] array = new int[args.length - 1];

        for (int i = 0; i < args.length - 1; i++) {
            array[i] = Integer.parseInt(args[i]);  
        }

        int target = Integer.parseInt(args[args.length - 1]);
        boolean result = searchNumber(array, target);
        System.out.println(result);
    }

    public static boolean searchNumber(int[] array, int target) {
        /**
        * Searches for a target in an array and returns true if found, false otherwise
        *
        * @param array  The array to search in
        * @param target The target to search for
        * @return true if the target is found in the array, false otherwise
        */
        return false;
    }
}"""
