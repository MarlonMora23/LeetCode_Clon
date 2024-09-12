import re
from problems.MyApp import test_problem


def validate_password(password: str) -> bool:
    """
    Validates if a given password meets the requirements specified in the problem's metadata.

    Args:
        password: The password to be tested.

    Returns:
        A boolean indicating whether the password is valid or not.
    """
    # At least 8 characters
    if len(password) < 8:
        return False

    # At least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # At least one digit
    if not re.search(r"\d", password):
        return False

    # At least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


def test_problem_2(data: dict) -> tuple:
    """
    Tests problem 1 in the given language.

    Args:
        data: A dictionary containing the code to be tested and the language.

    Returns:
        A tuple containing the result of the test in JSON format and a status code.
    """
    test_list: list[str] = [
        # Casos exitosos
        "Password1!",  # Cumple con todas las reglas
        "Valid123$",  # Cumple con todas las reglas
        "Str0ngP@ssw0rd",  # Cumple con todas las reglas
        # Casos fallidos
        "short1!",  # Menos de 8 caracteres
        "nouppercase1!",  # Sin mayúsculas
        "NOLOWERCASE1!",  # Sin minúsculas
        "NoSpecial123",  # Sin caracteres especiales
        "NoDigits!",  # Sin dígitos
        "",  # Contrasena vacía
        "12345678",  # Solo números, sin letras ni caracteres especiales
        "abcdefgh",  # Solo letras minúsculas, sin números ni caracteres especiales
        "ABCDEFGH",  # Solo letras mayúsculas, sin números ni caracteres especiales
        "!@#$%^&*()",
    ]

    return test_problem(
        data=data,
        test_list=test_list,
        problem_id=2,
        test_function=validate_password,
        python_func_name="validate_password",
        java_func_name="validatePassword",
    )
