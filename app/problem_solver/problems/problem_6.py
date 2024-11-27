from app.problem_solver.interfaces.i_problem import IProblem


class Problem6(IProblem):
    """
    Represents the problem of checking if a given string is a palindrome.
    
    The problem is to write a function that checks whether a string is a palindrome.
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
        return "¿Es palindromo?"
    
    def get_problem_description(self) -> str:
        """
        Returns:
            str: The description of the problem.
        """
        return "Escribe una función que determine si una cadena es un palíndromo. Un palíndromo es una cadena que se lee igual de izquierda a derecha que de derecha a izquierda."
    
    def get_detailed_problem_description(self) -> str:
        return "Un palíndromo es una cadena que se lee igual de izquierda a derecha que de derecha a izquierda. Escribe en la consola un programa que determine si una cadena es un palíndromo. La función recibe una cadena como argumento y devuelve Verdadero si la cadena es un palíndromo, Falso si no lo es."
    
    def get_problem_difficulty(self) -> str:
        """
        Returns:
            str: The difficulty of the problem.
        """
        return "easy"

    def get_test_list(self) -> list:
        """
        Returns a list of test cases for the problem.

        The list contains strings and whether they are palindromes or not.

        Returns:
            list: A list of test cases.
        """
        return ["racecar", "Palindrome",
            "A man, a plan, a canal, Panama",
            "",  # An empty string is a palindrome
            "No lemon, no melon",
            "Hello",
            "Was it a car or a cat I saw?",
            "Able was I, I saw Elba"
        ]
    
    def get_submission_test_list(self) -> list:
        return [
            "A Santa at NASA.",
            "Do geese see God?",
            "Mr. Owl ate my metal worm.",
            "Do nine men interpret? Nine men, I nod.",
            "Madam, I'm Adam.",
            "A man, a plan, a cat, a canal, Panama!",
            "Was it a car or a cat I saw?",
            "No 'x' in Nixon.",
            "Able was I ere I saw Elba.",
            "A Toyota's a Toyota.",
            "Never odd or even.",
            "Madam, in Eden, I'm Adam."
        ]

    def get_expected_output(self, submit) -> list:
        """
        Returns a list of expected outputs for the problem.

        The expected output is a list of booleans indicating if the string is a palindrome.

        Returns:
            list: A list of expected outputs.
        """
        test_function = self.get_test_function()
        test_cases = self.get_test_list() if not submit else self.get_submission_test_list()
        return [test_function(i) for i in test_cases]
    
    def get_python_function_name(self) -> str:
        return "is_palindrome"
    
    def get_java_function_name(self) -> str:
        return "isPalindrome"
    
    def get_ruby_function_name(self) -> str:
        return "is_palindrome"
    
    def get_test_function(self) -> callable:

        def is_palindrome(s: str) -> bool:
            """
            Checks if a given string is a palindrome.

            Args:
                s: The string to check.

            Returns:
                bool: True if the string is a palindrome, False otherwise.
            """
            # Remove non-alphanumeric characters and convert to lowercase
            cleaned = ''.join(char.lower() for char in s if char.isalnum())
            return cleaned == cleaned[::-1]
        
        return is_palindrome

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
            "def is_palindrome(s: str) -> bool:\n"
            "    # Your code goes here\n"
            "    return False\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem.

        Returns:
            str: The initial Java code for the problem.
        """
        return (
            "public static boolean isPalindrome(String s) {\n"
            "    // Your code goes here\n"
            "    return false;\n"
            "}\n"
        )
    
    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class isPalindrome {\n"
            "    public static void main(String[] args) {\n"
            "        String s = args[0];\n"
            "        boolean result = isPalindrome(s);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )
    
    def get_initial_ruby_code(self) -> str:
        return (
            "def is_palindrome(s)\n"
            "    # Your code goes here\n"
            "    return false\n"
            "end\n"
        )
    
    def get_testing_ruby_code(self) -> str:
        return (
            "input = ARGV[0]\n"
            "result = is_palindrome(input)\n"
            "puts result\n"
        )
    
    def is_boolean(self) -> bool:
        return True
    
    def is_integer(self) -> bool:
        return False
