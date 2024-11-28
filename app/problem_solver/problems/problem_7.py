from app.problem_solver.interfaces.i_problem import IProblem


class Problem7(IProblem):
    """
    Represents the problem of converting a monetary amount to its English word representation.

    The problem is to write a function that converts a given amount in dollars and cents
    to its English words representation.
    """

    def get_problem_id(self) -> int:
        """
        Returns:
            int: The id of the problem.
        """
        return 7

    def get_problem_name(self) -> str:
        """
        Returns:
            str: The name of the problem.
        """
        return "Convertir dinero a inglés"

    def get_problem_description(self) -> str:
        """
        Returns:
            str: The description of the problem.
        """
        return "Escribe una función que convierta un monto monetario dado en su representación en palabras en inglés."

    def get_detailed_problem_description(self) -> str:
        return """
            La función debe recibir como parámetro un monto monetario en formato numérico (por ejemplo, 123.45)
            y debe devolver una cadena de texto que represente el monto en inglés
            (por ejemplo, "one hundred twenty-three dollars and forty-five cents").
            """

    def get_problem_difficulty(self) -> str:
        """
        Returns:
            str: The difficulty of the problem.
        """
        return "hard"

    def get_test_list(self) -> list:
        """
        Returns:
            list: A list of test cases.
        """
        return [0, 0.5, 1, 1.2, 4.2, 10]

    def get_submission_test_list(self) -> list:
        return [0.01, 5.67, 12.34, 100.00, 1234.56, 1000.99]

    def get_expected_output(self, submit: bool = False) -> list:
        """
        Returns a list of expected outputs for the problem.

        The expected output is a list of booleans indicating whether the number is prime or not.

        Returns:
            list: A list of expected outputs.
        """
        test_function: callable = self.get_test_function()
        test_list = (
            self.get_test_list() if not submit else self.get_submission_test_list()
        )

        return [test_function(i) for i in test_list]

    def get_python_function_name(self) -> str:
        return "money_to_english"

    def get_java_function_name(self) -> str:
        """
        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Java.
        """
        return "moneyToEnglish"

    def get_ruby_function_name(self) -> str:
        """
        Returns:
            str: The name of the function in the problem that is expected
            to be implemented in Ruby.
        """
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
        """
        Returns a dictionary containing metadata about the problem.

        The dictionary should contain the following keys:

        - allow_recursion (bool): Whether the problem allows recursion.
        - disallowed_keywords (list[str]): A list of keywords that are not allowed in the solution.

        Returns:
            dict: A dictionary containing the metadata about the problem.
        """

        return {
            "allow_recursion": True,
            "disallowed_keywords": ["__builtins__", "while"],
        }

    def get_initial_python_code(self) -> str:
        """
        Returns the initial Python code for the problem, formatted in a way
        that improves readability.

        Returns:
            str: The initial Python code for the problem.
        """
        return (
            "def money_to_english(amount: float) -> bool:\n"
            "    # Your code goes here\n"
            "    return None\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem, formatted for improved readability.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "public static String moneyToEnglish(float amount) {\n"
            "    // Your code goes here\n"
            "    return null;\n"
            "}\n"
        )

    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class moneyToEnglish {\n"
            "    public static void main(String[] args) {      \n"
            "        float amount = Float.parseFloat(args[0]);        \n"
            "        String result = moneyToEnglish(amount);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )

    def get_initial_ruby_code(self) -> str:
        """
        Returns the initial Ruby code for the problem, formatted for improved readability.

        Returns:
            str: The initial Ruby code for the problem.
        """
        return (
            "def money_to_english(amount)\n"
            "    # Your code goes here\n"
            "    return nil\n"
            "end\n"
        )

    def get_testing_ruby_code(self) -> str:
        return (
            "input = ARGV[0].to_i\n" 
            "result = money_to_english(input)\n" 
            "puts result\n"
        )

    def is_boolean(self):
        return False

    def is_integer(self):
        return False
