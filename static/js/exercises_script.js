const get_initial_codes = () => {
    const codeDataElement = document.getElementById('initial-code-data');
    return {
        python: JSON.parse(codeDataElement.getAttribute('data-python')),
        java: JSON.parse(codeDataElement.getAttribute('data-java')),
    };
}

const get_last_codes = () => {
    const codeDataElement = document.getElementById('initial-code-data');
    return {
        python: JSON.parse(codeDataElement.getAttribute('data-last-python-code')),
        java: JSON.parse(codeDataElement.getAttribute('data-last-java-code'))
    };
}

const initializeCodeMirror = () => {
    const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
        lineNumbers: true,
        mode: "python",
        theme: "dracula",
        matchBrackets: true,
        autoCloseBrackets: true,
        tabSize: 4
    });

    // Get the initial code from the hidden div
    const initial_codes = get_initial_codes();
    const last_codes = get_last_codes();

    // Load the last sent code if it exists, otherwise load the initial code
    const selectedLanguage = 'python';
    const lastCode = last_codes[selectedLanguage];

    if (lastCode !== null && lastCode !== "None" && lastCode !== "") {
        editor.setValue(lastCode);
    } else {
        editor.setValue(initial_codes[selectedLanguage]);
    }

    return editor;
}

// Load the initial code from the editor according to the problem and the selected language
const change_initial_code = (selected_language) => {
    const initial_codes = get_initial_codes();
    const last_codes = get_last_codes();
    const mode = selected_language === 'python' ? 'python' : 'text/x-java';

    editor.setOption("mode", mode);

    const lastCode = last_codes[selected_language];

    if (lastCode !== null && lastCode !== "None" && lastCode !== "") {
        editor.setValue(lastCode);
    } else {
        editor.setValue(initial_codes[selected_language]);
    }
}

const reload_last_code = () => {
    if (get_last_codes()[document.querySelector('#language-select').value] === null) {
        Swal.fire({
            icon: 'error',
            title: 'No has subido código',
            text: 'No hay código guardado para este problema',
        })
    } else {
        editor.setValue(get_last_codes()[document.querySelector('#language-select').value]);
    }
}

const reload_initial_code = () => {
    editor.setValue(get_initial_codes()[document.querySelector('#language-select').value]);
}

const run_code = (url) => {
    // Get problem features
    const problem_id = document.getElementById('exercise-number').getAttribute('data-exercise');
    const language = document.querySelector('#language-select').value;
    const code = editor.getValue();

    // Get the output area
    const output = document.querySelector('.output__message');

    output.innerHTML = 'Cargando...';


    // Send the code to the server as a POST request
    fetch(url, {
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
            if (data['error']) {
                if (data['error'] === 'Para subir una solución, primero inicia sesión.') {
                    title = 'Debes iniciar sesión';
                }
                // Show the error message
                Swal.fire({
                    icon: 'error',
                    title: title,
                    text: data['error'],
                })
                output.innerHTML = '>_';
                return;
            }

            // Update the output area
            const result = document.createElement('p');
            result.classList.add('output__line');

            if (data['result'] === 'Exito') {
                result.classList.add('output__success');
            } else {
                result.classList.add('output__failure');
            }

            result.innerHTML = `<b style="font-size: 1.2rem">${data['result']}</b> `;

            const feedback = document.createElement('p');
            feedback.classList.add('output__line');
            feedback.innerHTML = data['feedback'];

            const expectedOutputTitle = document.createElement('p');
            expectedOutputTitle.innerHTML = '<b style="font-size: 0.8rem">Resultados esperados:</b>';

            const expectedOutput = document.createElement('p');
            expectedOutput.classList.add('output__line');
            expectedOutput.textContent = data['expected_output'];

            const testedOutputTitle = document.createElement('p');
            testedOutputTitle.innerHTML = '<b style="font-size: 0.8rem">Resultados obtenidos:</b>';

            const testedOutput = document.createElement('p');
            testedOutput.classList.add('output__line');
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

const logout = async (event) => {
    event.preventDefault();

    const currentUrl = window.location.href;
    console.log(currentUrl);

    try {
        const response = await fetch('/logout', {
            method: 'POST',
        });

        if (response.ok) {
            Swal.fire({
                icon: 'success',
                title: 'Cierre de sesión exitoso',
                showConfirmButton: false,
                timer: 1000
            }).then(() => {
                window.location.href = currentUrl;
            })

        } else {
            const errorData = await response.json();
            Swal.fire({
                icon: 'error',
                title: 'Cierre de sesión fallido',
                text: errorData.message
            })
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

const run_app = () => {
    const run_button = document.getElementById('run-button');
    const submit_button = document.getElementById('submit-button');
    const language_select = document.querySelector('#language-select');
    const logout_button = document.getElementById('logout-button');
    const reload_initial_code_button = document.getElementById('reload-initial-code-button');
    const reload_last_code_button = document.getElementById('reload-last-code-button');
    editor = initializeCodeMirror();

    run_button.addEventListener('click', function () {
        run_code('/run');
    });
    submit_button.addEventListener('click', function () {
        run_code('/submit');
    });

    language_select.addEventListener('change', function () {
        const selected_language = language_select.value;
        change_initial_code(selected_language);
    });

    reload_initial_code_button.addEventListener('click', reload_initial_code);
    reload_last_code_button.addEventListener('click', reload_last_code);
    logout_button.addEventListener('click', logout);
}

document.addEventListener('DOMContentLoaded', run_app);

