from app.problem_solver.interfaces.i_problem import IProblem


class Problem4(IProblem):
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
        return 4  

    def get_problem_name(self) -> str:
        """
        Returns:
            str: The name of the problem.
        """
        return "Entero a número romano"
    
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
        return [1, 4, 9, 58, 1994, 3999, 4000, 0, -5]

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
        return "int_to_roman"
    
    def get_java_function_name(self) -> str:
        return "intToRoman"
    
    def get_ruby_function_name(self) -> str:
        return "int_to_roman"
    
    def get_test_function(self) -> callable:
    
        def int_to_roman(num: int) -> str:
            """
            Converts an integer to a Roman numeral.

            Args:
                num: The integer to convert.

            Returns:
                str: The Roman numeral equivalent, or None if invalid.
            """
            if not isinstance(num, int) or num <= 0 or num > 3999:
                return None

            valores = [
                (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
                (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
                (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
            ]
            
            resultado = ""
            for valor, simbolo in valores:
                while num >= valor:
                    resultado += simbolo
                    num -= valor
            return resultado
        
        return int_to_roman
    
    def get_metadata(self) -> dict:
        return {
            "allow_recursion": False,
            "disallowed_keywords": ["__builtins__"],
        }

    def get_initial_python_code(self) -> str:
        """
        Returns the initial Python code for the problem.

        Returns:
            str: The initial Python code for the problem.
        """
        return (
            "def int_to_roman(num: int) -> str:\n"
            "    # Your code goes here\n"
            "    return None\n\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "public static String intToRoman(int num) {\n"
            "    // Your code goes here\n"
            "    return null;\n"
            "}\n\n"
        )
    
    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class intToRoman {\n"
            "    public static void main(String[] args) {\n"
            "        int num = Integer.parseInt(args[0]);\n"
            "        String result = intToRoman(num);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )
    
    def get_initial_ruby_code(self) -> str:
        return (
            "def int_to_roman(num)\n"
            "    # Your code goes here\n"
            "    return false\n"
            "end\n\n"
        )
    
    def get_testing_ruby_code(self) -> str:
        return (
            "input = ARGV[0].to_i\n"
            "result = int_to_roman(input)\n"
            "puts result\n"
        )
    
    def is_boolean(self) -> bool:
        return False
    
    def is_integer(self) -> bool:
        return False
