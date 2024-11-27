// Get the supported languages dynamically from the backend
const getSupportedLanguages = () => {
    const languageDataElement = document.getElementById('language-data');
    return JSON.parse(languageDataElement.getAttribute('data-languages'));
};

// Initialize the language selector
const initializeLanguageSelector = () => {
    const languageSelect = document.getElementById('language-select');
    const supportedLanguages = getSupportedLanguages();

    // Populate the select options dynamically
    supportedLanguages.forEach(language => {
        const option = document.createElement('option');
        option.value = language.value;
        option.textContent = language.name;
        languageSelect.appendChild(option);
    });

    // Set the default language to the first option
    languageSelect.value = supportedLanguages[0].value;
};

// Get the initial code for all supported languages
const getInitialCodes = () => {
    const codeDataElement = document.getElementById('initial-code-data');
    const initialCodes = {};

    // Obtén los lenguajes soportados
    getSupportedLanguages().forEach(language => {
        initialCodes[language.value] = JSON.parse(
            codeDataElement.getAttribute(`data-${language.value}`)
        );
    });

    return initialCodes;
};

const getLastCodes = () => {
    const codeDataElement = document.getElementById('initial-code-data');
    const lastCodes = {};

    // Obtén los lenguajes soportados
    getSupportedLanguages().forEach(language => {
        lastCodes[language.value] = JSON.parse(
            codeDataElement.getAttribute(`data-last-${language.value}`)
        );
    });

    return lastCodes;
};


// Initialize CodeMirror and load the selected language code
const initializeCodeMirror = () => {
    const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
        lineNumbers: true,
        theme: "dracula",
        indentUnit: 4,
        indentWithTabs: true,
        lineWrapping: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        tabSize: 4
    });

    const initialCodes = getInitialCodes();
    const lastCodes = getLastCodes();
    const languageSelect = document.getElementById('language-select');

    // Set the initial editor content and mode
    const setEditorContent = (language) => {
        const selectedLanguage = getSupportedLanguages().find(lang => lang.value === language);
        editor.setOption("mode", selectedLanguage.mode);

        const lastCode = lastCodes[language];
        editor.setValue(lastCode && lastCode !== "None" ? lastCode : initialCodes[language]);
    };

    // Listen to language changes and update the editor
    languageSelect.addEventListener('change', () => {
        const selectedLanguage = languageSelect.value;
        setEditorContent(selectedLanguage);
    });

    // Initialize with the default language
    setEditorContent(languageSelect.value);

    return editor;
};

// Load the initial code from the editor according to the problem and the selected language
const changeInitialCode = (editor, selected_language) => {
    const initial_codes = getInitialCodes();
    const last_codes = getLastCodes();
    const mode = selected_language === 'python' ? 'python' : 'text/x-java';

    editor.setOption("mode", mode);

    const lastCode = last_codes[selected_language];

    if (lastCode !== null && lastCode !== "None" && lastCode !== "") {
        editor.setValue(lastCode);
    } else {
        editor.setValue(initial_codes[selected_language]);
    }
}

const reloadLastCode = (editor) => {
    if (getLastCodes()[document.querySelector('#language-select').value] === null) {
        Swal.fire({
            icon: 'error',
            title: 'No has subido código',
            text: 'No hay código guardado para este problema',
        })
    } else {
        editor.setValue(getLastCodes()[document.querySelector('#language-select').value]);
    }
}

const reloadInitialCode = (editor) => {
    editor.setValue(getInitialCodes()[document.querySelector('#language-select').value]);
}

const changeCodemirrorCode = (editor, code) => {
    editor.setValue(code);
}

const runCode = (url, editor) => {
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
            const title = data['error'] === 'Para subir una solución, primero inicia sesión.' ? 'Debes iniciar sesión' : 'Error';
            // Show the error message
            Swal.fire({
                icon: 'error',
                title: title,
                text: data['error'],
            });
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

const runApp = () => {
    const run_button = document.getElementById('run-button');
    const submit_button = document.getElementById('submit-button');
    const language_select = document.querySelector('#language-select');
    const logout_button = document.getElementById('logout-button');
    const reload_initial_code_button = document.getElementById('reload-initial-code-button');
    const reload_last_code_button = document.getElementById('reload-last-code-button');
    const description_btn = document.getElementById('description-btn');
    const submissions_btn = document.getElementById('submissions-btn');
    const problem_description = document.getElementById('problem-description');
    const problem_submissions = document.getElementById('problem-submissions');
    const submissions_btns = document.querySelectorAll('.submission-btn');
    const description_title = document.getElementById('description-title');
    const submissions_title = document.getElementById('submissions-title');

    initializeLanguageSelector();
    const editor = initializeCodeMirror();

    description_btn.addEventListener('click', function () {
        if (problem_description.classList.contains('hidden')) {
            problem_description.classList.remove('hidden');
            problem_submissions.classList.add('hidden');
            submissions_title.classList.add('faded');
            description_title.classList.remove('faded');
        }
    });
    
    submissions_btn.addEventListener('click', function () {
        if (problem_submissions.classList.contains('hidden')) {
            problem_submissions.classList.remove('hidden');
            problem_description.classList.add('hidden');
            submissions_title.classList.remove('faded');
            description_title.classList.add('faded');
        }
    });

    submissions_btns.forEach(button => {
        button.addEventListener('click', () => {
            const code = JSON.parse(button.getAttribute('submission-code'));
            changeCodemirrorCode(editor, code);
        });
    });

    run_button.addEventListener('click', function () {
        runCode('/run', editor);
    });

    submit_button.addEventListener('click', function () {
        runCode('/submit', editor);
    });

    language_select.addEventListener('change', function () {
        const selected_language = language_select.value;
        changeInitialCode(editor, selected_language);
    });

    reload_initial_code_button.addEventListener('click', function () {
        reloadInitialCode(editor);
    });

    reload_last_code_button.addEventListener('click', function () {
        reloadLastCode(editor);
    });
    
    logout_button.addEventListener('click', logout);
}

document.addEventListener('DOMContentLoaded', runApp);

