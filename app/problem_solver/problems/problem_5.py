from app.problem_solver.interfaces.i_problem import IProblem


class Problem5(IProblem):
    """
    Represents the problem of converting numbers between integers and Roman numerals.
    
    The problem is to write two functions:
    1. Convert an integer to a Roman numeral.
    2. Convert a Roman numeral to an integer.
    """

    def get_problem_id(self) -> int:
        """
        Returns the id of the problem.

        Returns:
            int: The id of the problem.
        """
        return 5

    def get_problem_name(self) -> str:
        """
        Returns:
            str: The name of the problem.
        """
        return "Numero romano a entero"
    
    def get_problem_description(self) -> str:
        """
        Returns:
            str: The description of the problem.
        """
        return "Escribe una función que convierta un número entero a un número romano."
    
    def get_problem_difficulty(self) -> str:
        """
        Returns:
            str: The difficulty of the problem.
        """
        return "medium"

    def get_test_list(self) -> list:
        """
        Returns a list of test cases for the problem.

        The list contains integers and their corresponding Roman numeral conversions.

        Returns:
            list: A list of test cases.
        """
        return ["I", "IV", "IX", "LVIII", "MCMXCIV","MMMCMXCIX"]

    def get_expected_output(self) -> list:
        """
        Returns a list of expected outputs for the problem.

        The expected output is a list of tuples with both integer to Roman conversion and vice versa.

        Returns:
            list: A list of expected outputs.
        """
        test_function = self.get_test_function()
        test_cases = self.get_test_list()
        return [test_function(i) for i in test_cases]
    
    def get_python_function_name(self) -> str:
        return "roman_to_int"
    
    def get_java_function_name(self) -> str:
        return "romanToInt"
    
    def get_ruby_function_name(self) -> str:
        return "roman_to_int"
    
    def get_test_function(self) -> callable:

        def roman_to_int(roman: str) -> int:
            """
            Converts a Roman numeral to an integer.

            Args:
                roman: The Roman numeral to convert.

            Returns:
                int: The integer equivalent, or None if invalid.
            """
            if not isinstance(roman, str) or roman == "":
                return None

            valores = {
                'M': 1000, 'CM': 900, 'D': 500, 'CD': 400, 
                'C': 100, 'XC': 90, 'L': 50, 'XL': 40, 
                'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1
            }
            
            i = 0
            resultado = 0
            while i < len(roman):
                if i + 1 < len(roman) and roman[i:i+2] in valores:
                    resultado += valores[roman[i:i+2]]
                    i += 2
                elif roman[i] in valores:
                    resultado += valores[roman[i]]
                    i += 1
                else:
                    return None  # Invalid Roman numeral
            return resultado
        
        return roman_to_int
    
    def get_metadata(self) -> dict:
        return {
            "allow_recursion": False,
            "disallowed_keywords": ["__builtins__"]
        }

    def get_initial_python_code(self) -> str:
            """
            Returns the initial Python code for the problem.

            Returns:
                str: The initial Python code for the problem.
            """
            return (
                "def roman_to_int(num: int) -> str:\n"
                "    # Your code goes here\n"
                "    return 0\n\n"
            )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "public static int romanToInt(String num) {\n"
            "    // Your code goes here\n"
            "    return 0;\n"
            "}\n\n"
        )
    
    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class romanToInt {\n"
            "    public static void main(String[] args) {\n"
            "        String num = args[0];\n"
            "        int result = romanToInt(num);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )
    
    def get_initial_ruby_code(self) -> str:
        return (
            "def roman_to_int(num)\n"
            "    # Your code goes here\n"
            "    return 0\n"
            "end\n\n"
        )
    
    def get_testing_ruby_code(self) -> str:
        return (
            "input = ARGV[0].to_i\n"
            "result = roman_to_int(input)\n"
            "puts result\n"
        )
    
    def is_boolean(self) -> bool:
        return False
    
    def is_integer(self) -> bool:
        return True

