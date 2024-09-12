const display_initial_code_1 = (language) => {
    if (language === 'python') {
        document.getElementById('editor').value =
            `def is_prime_number(n: int) -> bool:
    """
    Checks if a given number is a prime number.

    Parameters
    ----------
    n : int
        The number to be checked for primality.

    Returns
    -------
    bool
        True if the number is a prime number, False otherwise.
    """
    return None
    `}

    if (language === 'java') {
        document.getElementById('editor').value =
            `package temp;

public class isPrimeNumber {
    public static void main(String[] args) {      
        int n = Integer.parseInt(args[0]);        
        boolean result = isPrimeNumber(n);
        System.out.println(result);
    }

    public static boolean isPrimeNumber(int n) {
        // Your code goes here
        return false;
    }
}
    `}
}


const display_initial_code_2 = (language) => {
    if (language === 'python') {
        document.getElementById('editor').value =
            `def validate_password(password: str) -> bool:
    """
    Validates if a given password meets the requirements specified in the problem's metadata.

    Args:
        password: The password to be tested.

    Returns:
        A boolean indicating whether the password is valid or not.
    """
    return None
    `}

    if (language === 'java') {
        document.getElementById('editor').value =
            `package temp;

public class validatePassword {
    public static void main(String[] args) {      
        String n = String.valueOf(args[0]);        
        boolean result = validatePassword(n);
        System.out.println(result);
    }

    public static boolean validatePassword(String n) {
        // Your code goes here
        return false;
    }
}
    `}
}


const display_initial_code_3 = (language) => {
    if (language === 'python') {
        document.getElementById('editor').value =
            `def search_number(array: list, target: int):
    """
    Searches for a target in an array and returns True if found, False otherwise
    
    Parameters
    ----------
    array : list
        The array to search in
    target : int
        The target to search for
    
    Returns
    -------
    bool
        True if the target is found in the array, False otherwise
    """
    return target in array
    `}

    if (language === 'java') {
        document.getElementById('editor').value =
            `package temp;

public class isPrimeNumber {
    public static void main(String[] args) {      
        int n = Integer.parseInt(args[0]);        
        boolean result = isPrimeNumber(n);
        System.out.println(result);
    }

    public static boolean isPrimeNumber(int n) {
        // Your code goes here
        return false;
    }
}
    `}
}


// Load the initial code from the editor according to the problem and the selected language
const changeInitialCode = (language) => {
    const problem_id = document.getElementById('exercise-number').getAttribute('data-exercise');
    console.log('clieckeado')

    if (problem_id == 1) {
        display_initial_code_1(language)
    }

    if (problem_id == 2) {
        display_initial_code_2(language)
    }

    if (problem_id == 3) {
        display_initial_code_3(language)
    }
}



const submit_code = () => {
    // Get problem features
    const problem_id = document.getElementById('exercise-number').getAttribute('data-exercise');
    const language = document.querySelector('#language-select').value;
    const code = document.querySelector('#editor').value;

    // Get the output area
    const output = document.querySelector('.output__area');

    output.innerHTML = 'Cargando...';


    // Send the code to the server as a POST request
    fetch('http://127.0.0.1:8080/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Send the code in JSON format
        },
        body: JSON.stringify({
            'problem_id': problem_id,
            'language': language,
            'code': code
        })
    })
        .then(response => response.json())
        .then(data => {
            // Update the output area
            const result = document.createElement('p');
            result.classList.add('output__message');
            result.innerHTML = `<b>Result:</b> ${data['result']}`;

            const feedback = document.createElement('p');
            feedback.classList.add('output__message');
            feedback.innerHTML = `<b>Feedback:</b> ${data['feedback']}`;

            const expectedOutputTitle = document.createElement('p');
            expectedOutputTitle.innerHTML = '<b>Expected Output:</b>';

            const expectedOutput = document.createElement('p');
            expectedOutput.classList.add('output__message');
            expectedOutput.textContent = data['expected_output'];

            const testedOutputTitle = document.createElement('p');
            testedOutputTitle.innerHTML = '<b>Tested Output:</b>';

            const testedOutput = document.createElement('p');
            testedOutput.classList.add('output__message');
            testedOutput.textContent = data['tested_output'];

            output.innerHTML = '';
            output.appendChild(result);
            output.appendChild(feedback);
            output.appendChild(expectedOutputTitle);
            output.appendChild(expectedOutput);
            output.appendChild(testedOutputTitle);
            output.appendChild(testedOutput);

            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
            output.innerHTML = 'Error: ' + error;
        });
}


const run_app = () => {
    const submit_button = document.getElementById('run-button');
    const language_select = document.querySelector('#language-select')

    // When the user clicks on the button, submit the code
    submit_button.addEventListener('click', submit_code);

    // When the user changes the language, change the initial code
    language_select.addEventListener('change', function() {
        const selected_language = language_select.value;
        changeInitialCode(selected_language); 
    });
}

document.addEventListener('DOMContentLoaded', run_app);


