from problems.MyApp import test_problem
import random
from typing import List, Tuple
from problems.i_problem import IProblem


class Problem3(IProblem):
    def get_problem_id(self) -> int:
        return 3

    def get_test_list(self) -> list:
        return [[3, 4, 7, 10, 11, 12, 19, 20, 23, 24, 29, 33, 37]]

    def get_target(self) -> any:
        return [3, 5, 12, 22, 37]

    def get_n_test_cases(self) -> int:
        return 5

    def get_python_function_name(self) -> str:
        return "search_number"

    def get_java_function_name(self) -> str:
        return "searchNumber"

    def get_test_function(self) -> callable:
        return search_number

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

# class Generator:
#     def _init_(self):
#         # Initialize arrays with random numbers and compute cumulative sums
#         self.arrays: List[List[int]] = [
#             [random.randint(0, 100) for _ in range(10)] for _ in range(10)
#         ]
#         self.arrays_sum: List[List[int]] = [
#             self.cumulative_sum(array) for array in self.arrays
#         ]

#     def cumulative_sum(self, array: List[int]) -> List[int]:
#         cumulative_sum: List[int] = []
#         accumulator: int = 0
#         for num in array:
#             accumulator += num
#             cumulative_sum.append(accumulator)
#         return cumulative_sum

#     def search_number(self) -> Tuple[List[int], List[int]]:
#         numbers_in_array: List[int] = []
#         numbers_not_in_array: List[int] = []

#         for array in self.arrays_sum:
#             number_in: int = random.choice(array)
#             numbers_in_array.append(number_in)
#             number_not_in: int = random.randint(0, 100)
#             while number_not_in in array:
#                 number_not_in = random.randint(0, 100)
#             numbers_not_in_array.append(number_not_in)

#         return numbers_in_array, numbers_not_in_array


def test_problem_3(data: dict) -> tuple:
    """
    Tests problem 3 in the given language.

    Args:
        data: A dictionary containing the code to be tested and the language.

    Returns:
        A tuple containing the result of the test in JSON format and a status code.
    """
    problem = Problem3()
    return test_problem(problem, data)
