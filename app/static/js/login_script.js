const login = async (event) => {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const responseData = await response.json();
            window.location.href = responseData.redirect;
        } else {
            const errorData = await response.json();
            Swal.fire ({
                icon: 'error',
                title: 'Inicio de sesión fallido',
                text: errorData.message
            })
        }
    } catch (error) {
        console.error("Error:", error);
        Swal.fire ({
            icon: 'error',
            title: 'Inicio de sesión fallido',
            text: error
        })
    }
};

function run_app() {
    const login_form = document.getElementById('login-form');
    login_form.addEventListener('submit', login);
}

document.addEventListener('DOMContentLoaded', run_app);