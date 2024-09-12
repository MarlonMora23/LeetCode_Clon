from problems.MyApp import test_problem


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


def test_problem_1(data: dict) -> tuple:
    """
    Tests problem 1 in the given language.

    Args:
        data: A dictionary containing the code to be tested and the language.

    Returns:
        A tuple containing the result of the test in JSON format and a status code.
    """
    test_list: list[int] = [3, 4, 7, 10, 11, 12, 19, 20, 23, 24, 29, 33, 37]

    return test_problem(
        data=data,
        test_list=test_list,
        problem_id=1,
        test_function=is_prime_number,
        python_func_name="is_prime_number",
        java_func_name="isPrimeNumber",
    )
