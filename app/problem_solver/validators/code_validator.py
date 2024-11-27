import ast
import re
from typing import Dict, List, Any, Optional

NO_RECURSION_MSG = "La función no debe usar recursión."

class CodeValidator:
    """Class responsible for validating code against metadata requirements."""
    
    def __init__(self, code: str, metadata: Dict[str, Any]):
        self.code = code
        self.metadata = metadata
        
    def validate_keywords(self) -> Optional[Dict[str, str]]:
        """Validates if code contains any disallowed keywords."""
        disallowed_keywords: List[str] = self.metadata["disallowed_keywords"]
        
        for keyword in disallowed_keywords:
            if keyword in self.code:
                return {
                    "result": "Fallo",
                    "feedback": "El código contiene palabras no permitidas."
                }
        return None
        
    def validate_recursion(self, language: str, function_name: str = "") -> Dict[str, str]:
        """Validates recursion based on language and metadata requirements."""
        is_allowed_recursion: bool = self.metadata["allow_recursion"]
        
        if not is_allowed_recursion:
            if language == "python":
                return self._validate_python_recursion()
            
            if language == "java":
                return self._validate_java_recursion(function_name)
            
            if language == "ruby":
                return self._validate_ruby_recursion(function_name)
                
        return {"result": "Exito"}
    
    def _validate_python_recursion(self) -> Dict[str, str]:
        try:
            tree = ast.parse(self.code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):  # Verify if the node is a function
                    for child in ast.walk(node):  # Iterate over the children
                        if (
                            isinstance(child, ast.Call) and
                            isinstance(child.func, ast.Name) and  # Verify if the child is a function call
                            child.func.id == node.name  # Verify if the function name matches
                        ):
                            return {
                                "result": "Fallo",
                                "feedback": NO_RECURSION_MSG
                            }
        except Exception as e:
            return {
                "result": "Fallo",
                "feedback": str(e)
            }
        return {"result": "Exito"}
    
    def _validate_java_recursion(self, function_name: str) -> Dict[str, str]:
        matches = re.findall(function_name, self.code)
        if len(matches) > 3:
            return {
                "result": "Fallo",
                "feedback": NO_RECURSION_MSG
            }
        return {"result": "Exito"}
    
    def _validate_ruby_recursion(self, function_name: str) -> Dict[str, str]:
        """
        Validates that the Ruby code does not use recursion.
        
        Args:
            function_name (str): The name of the function to check.

        Returns:
            Dict[str, str]: Result and feedback regarding recursion usage.
        """
        try:
            # More precise regex to detect self-recursion
            pattern = rf"def\s+{re.escape(function_name)}.*?^.*?\b{function_name}\s*\("
            matches = re.search(pattern, self.code, re.MULTILINE | re.DOTALL)

            if matches:
                return {
                    "result": "Fallo",
                    "feedback": "La función no debe usar recursión."
                }
        except Exception as e:
            return {
                "result": "Fallo",
                "feedback": f"Error al validar recursión: {str(e)}"
            }
        return {"result": "Exito"}
