


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
    return None
    `}

    if (language === 'java') {
        document.getElementById('editor').value =
            `package temp;

public class searchNumber {
    public static void main(String[] args) {
        int[] array = new int[args[0].length()];
        for (int i = 0; i < args[0].length(); i++) {
            array[i] = Integer.parseInt(args[0].substring(i, i + 1));
        }
        int target = Integer.parseInt(args[1]);

        System.out.println("Searching for " + target + " in " + array);

        boolean result = searchNumber(array, target);
        System.out.println(result);
    }

    public static boolean searchNumber(int[] array, int target) {
        /**
         * Searches for a target in an array and returns true if found, false otherwise
         *
         * @param array  The array to search in
         * @param target The target to search for
         * @return true if the target is found in the array, false otherwise
         */
        for (int num : array) {
            if (num == target) {
                return true;
            }
        }
        return false;
    }
}   
    `}
}

const charge_initial_code = () => {
    document.getElementById('editor').value = initial_codes['python'];
}

// Load the initial code from the editor according to the problem and the selected language
const change_initial_code = (language) => {
    if (language === 'python') {
        document.getElementById('editor').value = initial_codes['python'];
    }

    else if (language === 'java') {
        document.getElementById('editor').value = initial_codes['java'];
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

    // Charge the initial code
    charge_initial_code();

    // When the user clicks on the button, submit the code
    submit_button.addEventListener('click', submit_code);

    // When the user changes the language, change the initial code
    language_select.addEventListener('change', function () {
        const selected_language = language_select.value;
        change_initial_code(selected_language);
    });
}

document.addEventListener('DOMContentLoaded', run_app);


