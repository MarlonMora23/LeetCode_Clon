import ast
import re
from typing import Dict, List, Any, Optional

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
                
        return {"result": "Exito"}
    
    def _validate_python_recursion(self) -> Dict[str, str]:
        try:
            tree = ast.parse(self.code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and any(
                    isinstance(child, ast.Call) and child.func.id == node.name
                    for child in ast.walk(node)
                ):
                    return {
                        "result": "Fallo",
                        "feedback": "La función no debe usar recursión."
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
                "feedback": "La función no debe usar recursión."
            }
        return {"result": "Exito"}