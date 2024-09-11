// Load the initial code from the editor according to the selected language
document.getElementById('language-select').addEventListener('change', function () {
    let language = this.value;

    if (language === 'python') {
        document.getElementById('editor').value =
            `def is_prime_number(n: int) -> bool:
    """
    Returns True if n is a prime number, False otherwise.
    """
    # your code goes here
    return None
    `}

    if (language === 'java') {
        document.getElementById('editor').value =
            `package temp;

public class PrimeCheck {
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
})


// Run the code
document.getElementById('run-button').addEventListener('click', function () {
    let problem_id = document.querySelector('[data-exercise]').getAttribute('data-exercise');
    let language = document.querySelector('#language-select').value;
    let code = document.querySelector('#editor').value;

    let output = document.querySelector('.output__area');

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
            let result = document.createElement('p');
            result.classList.add('output__message');
            result.innerHTML = `<b>Result:</b> ${data['result']}`;

            let feedback = document.createElement('p');
            feedback.classList.add('output__message');
            feedback.innerHTML = `<b>Feedback:</b> ${data['feedback']}`;

            let expectedOutputTitle = document.createElement('p');
            expectedOutputTitle.innerHTML = '<b>Expected Output:</b>';

            let expectedOutput = document.createElement('p');
            expectedOutput.classList.add('output__message');
            expectedOutput.textContent = data['expected_output'];

            let testedOutputTitle = document.createElement('p');
            testedOutputTitle.innerHTML = '<b>Tested Output:</b>';

            let testedOutput = document.createElement('p');
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
        });
});
