from app.problem_solver.interfaces.i_problem import IProblem


class Problem9(IProblem):

    def get_problem_id(self) -> int:
        """
        Retorna el id del problema.

        Returns:
            int: El id del problema.
        """
        return 9

    def get_problem_name(self) -> str:
        """
        Retorna el nombre del problema.

        Returns:
            str: El nombre del problema.
        """
        return "Suma de números pares"

    def get_problem_description(self) -> str:
        """
        Retorna la descripción del problema.

        Returns:
            str: La descripción del problema.
        """
        return "Escribe una función que sume todos los números pares en un arreglo y devuelva el resultado."
    
    def get_detailed_problem_description(self) -> str:
        return "Escribe una función en la consola que sume todos los números pares en un arreglo y devuelva el resultado."

    def get_problem_difficulty(self) -> str:
        """
        Retorna la dificultad del problema.

        Returns:
            str: La dificultad del problema.
        """
        return "easy"

    def get_test_list(self) -> list:
        """
        Retorna una lista de pruebas para el problema.

        Returns:
            list: Una lista de arreglos para los que se probará la función.
        """
        return [[1, 2, 3, 4], [0, 10, 15], [7, 8, 10, 13]]
    
    def get_submission_test_list(self) -> list:
        return [[2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
                [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29],
                [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]]

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
        """
        Retorna el nombre de la función en el problema que se espera sea implementada en Python.

        Returns:
            str: El nombre de la función en el problema.
        """
        return "sum_even_numbers"

    def get_java_function_name(self) -> str:
        """
        Retorna el nombre de la función en el problema que se espera sea implementada en Java.

        Returns:
            str: El nombre de la función en el problema.
        """
        return "sumEvenNumbers"
    
    def get_ruby_function_name(self) -> str:
        return "sum_even_numbers"

    def get_test_function(self) -> callable:
        """
        Retorna la función que realiza la prueba.

        Returns:
            callable: Una función que se puede utilizar para probar la implementación.
        """
        def sum_even_numbers(array: list):
            """
            Suma todos los números pares en un arreglo.

            Parameters
            ----------
            array : list
                El arreglo de números enteros.

            Returns
            -------
            int
                La suma de todos los números pares en el arreglo.
            """
            return sum(x for x in array if x % 2 == 0)
        
        return sum_even_numbers

    def get_metadata(self) -> dict:
        """
        Retorna un diccionario con metadatos sobre el problema.

        Returns:
            dict: Los metadatos del problema.
        """
        return {
            "allow_recursion": False,  
            "disallowed_keywords": ["eval", "exec", "__builtins__"]
        }

    def get_initial_python_code(self) -> str:
        """
        Retorna el código inicial en Python para el problema.

        Returns:
            str: El código inicial en Python para el problema.
        """
        return (
            "def sum_even_numbers(array: list):\n"
            "    # Your code goes here\n"
            "    return 0\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Retorna el código inicial en Java para el problema.

        Returns:
            str: El código inicial en Java para el problema.
        """
        return (
            "public static int sumEvenNumbers(int[] array) {\n"
            "    // Your code goes here.\n"
            "    return 0;\n"
            "}\n"
        )
    
    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class sumEvenNumbers {\n"
            "    public static void main(String[] args) {\n"
            "        String[] stringArray = args[0].split(\",\");\n"
            "        int[] array = new int[stringArray.length];\n"
            "        for (int i = 0; i < stringArray.length; i++) {\n"
            "            array[i] = Integer.parseInt(stringArray[i]);\n"
            "        }\n\n"
            "        int result = sumEvenNumbers(array);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )
    
    def get_initial_ruby_code(self) -> str:
        return (
            "def sum_even_numbers(array)\n"
            "    # Your code goes here\n"
            "    return 0\n"
            "end\n"
        )
    
    def get_testing_ruby_code(self) -> str:
        return (
            "input = ARGV[0].to_i\n"
            "result = sum_even_numbers(input)\n"
            "puts result\n"
        )
    
    def is_boolean(self) -> bool:
        return False
    
    def is_integer(self) -> bool:
        return True
