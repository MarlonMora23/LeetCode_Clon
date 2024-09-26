const initializeCodeMirror = () => {
    const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
        lineNumbers: true,        
        mode: "python",           
        theme: "dracula",         
        matchBrackets: true,      
        autoCloseBrackets: true, 
        tabSize: 4                
    });

     document.getElementById('language-select').addEventListener('change', function() {
        const selectedLanguage = this.value;
        const mode = selectedLanguage === 'python' ? 'python' : 'text/x-java'; 
        editor.setOption("mode", mode);
        change_initial_code(selectedLanguage); 
    });

    return editor;
}


const charge_initial_code = () => {
    code = initial_codes['python'];
    document.getElementById('editor').value = code;
    editor.setValue(code);
}

// Load the initial code from the editor according to the problem and the selected language
const change_initial_code = (language) => {
    if (language === 'python') {
        code = initial_codes['python'];
        document.getElementById('editor').value = initial_codes['python'];
        editor.setValue(code);
    }

    else if (language === 'java') {
        code = initial_codes['java'];
        document.getElementById('editor').value = initial_codes['java'];
        editor.setValue(code);
    }
}



const submit_code = () => {
    // Get problem features
    const problem_id = document.getElementById('exercise-number').getAttribute('data-exercise');
    const language = document.querySelector('#language-select').value;
    const code = editor.getValue(); 

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
    const language_select = document.querySelector('#language-select');
    editor = initializeCodeMirror();

    submit_button.addEventListener('click', submit_code);

    language_select.addEventListener('change', function() {
        const selected_language = language_select.value;
        change_initial_code(selected_language);
    });

    change_initial_code(language_select.value);
}

document.addEventListener('DOMContentLoaded', run_app);


