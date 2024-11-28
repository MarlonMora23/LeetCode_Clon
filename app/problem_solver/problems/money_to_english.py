from app.problem_solver.interfaces.i_problem import IProblem


class ProblemMoneyToEnglish(IProblem):
    """
    Represents the problem of converting a monetary amount to its English word representation.
    
    The problem is to write a function that converts a given amount in dollars and cents
    to its English words representation.
    """

    def get_problem_id(self) -> int:
        """
        Returns the id of the problem.

        Returns:
            int: The id of the problem.
        """
        return 6

    def get_problem_name(self) -> str:
        """
        Returns:
            str: The name of the problem.
        """
        return "Convertir monto monetario a inglés"
    
    def get_problem_description(self) -> str:
        """
        Returns:
            str: The description of the problem.
        """
        return "Escribe una función que convierta un monto monetario dado en su representación en palabras en inglés."
    
    def get_detailed_problem_description(self) -> str:
        return (
            "Dado un monto en dólares y centavos, escribe un programa que convierta el número a su representación en inglés. "
            "Por ejemplo, 123.45 se convierte en 'One Hundred Twenty-Three Dollars and Forty-Five Cents'."
        )
    
    def get_problem_difficulty(self) -> str:
        """
        Returns:
            str: The difficulty of the problem.
        """
        return "medium"

    def get_test_list(self) -> list:
        """
        Returns a list of test cases for the problem.

        Returns:
            list: A list of monetary amounts as floats.
        """
        return [0.01, 12.34, 100.00, 1234.56, 1_000_000.99]
    
    def get_expected_output(self, submit) -> list:
        """
        Returns a list of expected outputs for the problem.

        Returns:
            list: A list of strings representing monetary amounts in English.
        """
        test_function = self.get_test_function()
        test_cases = self.get_test_list()
        return [test_function(amount) for amount in test_cases]
    
    def get_python_function_name(self) -> str:
        return "money_to_english"
    
    def get_test_function(self) -> callable:

        def money_to_english(amount: float) -> str:
            """
            Converts a monetary amount to its English word representation.

            Args:
                amount: The monetary amount to convert.

            Returns:
                str: The English words representation of the amount.
            """
            if not isinstance(amount, (int, float)) or amount < 0:
                return "Invalid amount"
            
            def number_to_words(num: int) -> str:
                ones = [
                    "Zero", "One", "Two", "Three", "Four", 
                    "Five", "Six", "Seven", "Eight", "Nine"
                ]
                tens = [
                    "", "", "Twenty", "Thirty", "Forty", 
                    "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"
                ]
                teens = [
                    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", 
                    "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"
                ]

                def below_hundred(n):
                    if n < 10:
                        return ones[n]
                    elif n < 20:
                        return teens[n - 10]
                    else:
                        return tens[n // 10] + (" " + ones[n % 10] if n % 10 != 0 else "")

                def below_thousand(n):
                    if n < 100:
                        return below_hundred(n)
                    else:
                        return ones[n // 100] + " Hundred" + (
                            " " + below_hundred(n % 100) if n % 100 != 0 else ""
                        )

                if num == 0:
                    return "Zero"

                parts = []
                if num >= 1_000:
                    parts.append(below_thousand(num // 1_000) + " Thousand")
                    num %= 1_000
                if num > 0:
                    parts.append(below_thousand(num))
                
                return " ".join(parts)

            dollars = int(amount)
            cents = int(round((amount - dollars) * 100))
            
            dollar_part = number_to_words(dollars) + " Dollar" + ("s" if dollars != 1 else "")
            cent_part = (
                " and " + number_to_words(cents) + " Cent" + ("s" if cents != 1 else "")
                if cents > 0
                else ""
            )
            
            return dollar_part + cent_part

        return money_to_english
    
    def get_metadata(self) -> dict:
        return {
            "allow_recursion": False,
            "disallowed_keywords": ["eval", "exec", "__import__"]
        }

    def get_initial_python_code(self) -> str:
            """
            Returns the initial Python code for the problem.

            Returns:
                str: The initial Python code for the problem.
            """
            return (
                "def money_to_english(amount: float) -> str:\n"
                "    # Your code goes here\n"
                "    return \"\"\n\n"
            )
