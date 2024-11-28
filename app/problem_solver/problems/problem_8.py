from app.problem_solver.interfaces.i_problem import IProblem


class Problem8(IProblem):

    def get_problem_id(self) -> int:
        """
        Retorna el id del problema.

        Returns:
            int: El id del problema.
        """
        return 8
    
    def get_problem_name(self) -> str:
        """
        Retorna el nombre del problema.

        Returns:
            str: El nombre del problema.
        """
        return "Determinar si un número es perfecto"
    
    def get_problem_description(self) -> str:
        """
        Retorna la descripción del problema.

        Returns:
            str: La descripción del problema.
        """
        return (
            "Escribe una función que determine si un número entero positivo "
            "es un número perfecto. Un número perfecto es aquel cuya suma de "
            "sus divisores propios (excluyendo el número mismo) es igual al número."
        )
    
    def get_detailed_problem_description(self) -> str:
        """
        Retorna la descripción detallada del problema.

        Returns:
            str: La descripción detallada del problema.
        """
        return (
            "Un número perfecto es aquel cuya suma de sus divisores propios "
            "(excluyendo el número mismo) es igual al número. Escribe una función "
            "que determine si un número entero positivo es un número perfecto."
        )
    
    def get_problem_difficulty(self) -> str:
        """
        Retorna la dificultad del problema.

        Returns:
            str: La dificultad del problema.
        """
        return "medium"
    
    def get_test_list(self) -> list:
        """
        Retorna una lista de pruebas para el problema.

        Returns:
            list: Una lista de valores para los que se probará la función.
        """
        return [6, 28, 496, 12, 27]
    
    def get_submission_test_list(self) -> list:
        return [6, 28, 496, 12, 27, 3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

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
        return "is_perfect_number"
    
    def get_java_function_name(self) -> str:
        return "isPerfectNumber"
    
    def get_ruby_function_name(self) -> str:
        return "is_perfect_number"
    
    def get_test_function(self):
        def is_perfect_number(n: int) -> bool:
            """
            Determina si un número entero es un número perfecto.

            Parameters
            ----------
            n : int
                El número entero a verificar.

            Returns
            -------
            bool
                True si el número es perfecto, False en caso contrario.
            """
            if n <= 0:
                raise ValueError("El número debe ser positivo.")
            return sum(i for i in range(1, n) if n % i == 0) == n
        
        return is_perfect_number

    def get_metadata(self) -> dict:
        return {
            "allow_recursion": False,
            "disallowed_keywords": ["__builtins__"]
        }

    def get_initial_python_code(self) -> str:
        """
        Retorna el código inicial en Python para el problema.

        Returns:
            str: El código inicial en Python para el problema.
        """
        return (
            "def is_perfect_number(n: int) -> bool:\n"
            "    # Your code goes here\n"
            "    return None\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Retorna el código inicial en Java para el problema.

        Returns:
            str: El código inicial en Java para el problema.
        """
        return (
            "public static boolean isPerfectNumber(int n) {\n"
            "    // Your code goes here\n"
            "    return false;\n"
            "    }\n"
        )
    
    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class isPerfectNumber {\n"
            "    public static void main(String[] args) {\n"
            "        int n = Integer.parseInt(args[0]);\n"
            "        boolean result = isPerfectNumber(n);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )
    
    def get_initial_ruby_code(self) -> str:
        return (
            "def is_perfect_number(n)\n"
            "    # Your code goes here\n"
            "    return false\n"
            "end\n"
        )
    
    def get_testing_ruby_code(self) -> str:
        return (
            "input = ARGV[0].to_i\n"
            "result = is_perfect_number(input)\n"
            "puts result\n"
        )
    
    def is_boolean(self) -> bool:
        return True
    
    def is_integer(self) -> bool:
        return False
