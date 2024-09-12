// Load the initial code from the editor according to the selected language
document.getElementById('language-select').addEventListener('change', function () {
    const language = this.value;

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
})


// Run the code
document.getElementById('run-button').addEventListener('click', function () {
    const problem_id = document.getElementById('exercise-number').getAttribute('data-exercise');
    const language = document.querySelector('#language-select').value;
    const code = document.querySelector('#editor').value;

    const output = document.querySelector('.output__area');

    output.innerHTML = 'Cargando...';

    console.log(problem_id)

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
        });
});
