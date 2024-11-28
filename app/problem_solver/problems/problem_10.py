from app.problem_solver.interfaces.i_problem import IProblem


class Problem10(IProblem):
    """
    Represents the fifth exercise of the course.

    The fifth exercise is to write a function that constructs a 6-dimensional array filled with zeros.

    The Problem5 class implements the IProblem interface and provides a test list and expected
    output for the exercise.
    """

    def get_problem_id(self) -> int:
        """
        Returns the id of the problem.
        """
        return 10
    
    def get_problem_name(self) -> str:
        """
        Returns:
            str: The name of the problem.
        """
        return "Crear un array de 6 dimensiones"
    
    def get_problem_description(self) -> str:
        """
        Returns:
            str: The description of the problem.
        """
        return "Escribe una función que construya un array de 6 dimensiones lleno de ceros."
    
    def get_detailed_problem_description(self) -> str:
        return "Escribe en la consola un programa que construya un array de 6 dimensiones lleno de ceros. La función recibe un arreglo de enteros como argumento y devuelve el array construido."
    
    def get_problem_difficulty(self) -> str:
        """
        Returns:
            str: The difficulty of the problem.
        """
        return "hard"

    def get_test_list(self) -> list:
        """
        Returns a list of test cases for the problem.

        Returns:
            list: A list containing the sizes of the 6 dimensions.
        """
        return [[2, 2, 2, 2, 2]]  # Example: 2x2x2x2x2x2 array
    
    def get_submission_test_list(self) -> list:
        return [[3, 3, 3, 3, 3, 3]]

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
        Returns the Python function name for the problem.
        """
        return "create_6d_array"

    def get_java_function_name(self) -> str:
        """
        Returns the Java function name for the problem.
        """
        return "create6DArray"
    
    def get_ruby_function_name(self) -> str:
        """
        Returns the Ruby function name for the problem.
        """
        return "create_6d_array"

    def get_test_function(self) -> callable:
        """
        Returns the function to test user submissions.
        """
        def create_6d_array(dim_sizes: list) -> list:
            """
            Constructs a 6-dimensional array filled with zeros, given the size for each dimension.

            Parameters
            ----------
            dim_sizes : list
                A list containing the size for each of the 6 dimensions.

            Returns
            -------
            list
                A 6-dimensional array filled with zeros.
            """
            def create_dim(dims):
                if len(dims) == 1:
                    return [0] * dims[0]
                return [create_dim(dims[1:]) for _ in range(dims[0])]
            
            return create_dim(dim_sizes)
        
        return create_6d_array

    def get_metadata(self) -> dict:
        """
        Retorna un diccionario con metadatos sobre el problema.

        Returns:
            dict: Los metadatos del problema.
        """
        return {
            "allow_recursion": True,  
            "disallowed_keywords": ["eval", "exec", "__builtins__"]
        }

    def get_initial_python_code(self) -> str:
        """
        Returns the initial Python code for the problem.
        """
        return (
            "def create_6d_array(dim_sizes: list) -> list:\n"
            "    # Your code goes here\n"
            "    return None\n"
        )

    def get_initial_java_code(self) -> str:
        """
        Returns the initial Java code for the problem.
        """
        return (
            "public static int[][][][][][] create6DArray(int[] dimSizes) {\n"
            "    // Your code goes here\n"
            "    return null;\n"
            "}\n"
        )
    
    def get_testing_java_code(self) -> str:
        return (
            "package app.temp;\n\n"
            "public class create6DArray {\n"
            "    public static void main(String[] args) {\n"
            "        int[] dimSizes = new int[args.length];\n"
            "        for (int i = 0; i < args.length; i++) {\n"
            "            dimSizes[i] = Integer.parseInt(args[i]);\n"
            "        }\n"
            "        int[][][][][][] result = create6DArray(dimSizes);\n"
            "        System.out.println(result);\n"
            "    }\n\n"
        )
    
    def get_initial_ruby_code(self) -> str:
        return (
            "def create_6d_array(dim_sizes)\n"
            "    # Your code goes here\n"
            "    return nil\n"
            "end\n"
        )
    
    def get_testing_ruby_code(self) -> str:
        return (
            "dim_sizes = ARGV.map(&:to_i)\n"
            "result = create_6d_array(dim_sizes)\n"
            "puts result\n"
        )

    def is_boolean(self) -> bool:
        return False
    
    def is_integer(self) -> bool:
        return False
    