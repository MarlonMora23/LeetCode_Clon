const register = async (event) => {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            Swal.fire ({
                icon: 'success',
                title: 'Cuenta creada exitosamente',
                showConfirmButton: false,
                timer: 1000
            }).then(async () => {
                const responseData = await response.json();
        
                const loginResponse = await login(data.username, data.password);
        
                if (loginResponse.ok) {
                    window.location.href = responseData.redirect;
                } else {
                    const errorData = await loginResponse.json();
                    Swal.fire({
                        icon: 'error',
                        title: 'Inicio de sesión fallido',
                        text: errorData.message
                    });
                }
            });
        } else {
            const errorData = await response.json();
            Swal.fire ({
                icon: 'error',
                title: 'Cuenta no creada',
                text: errorData.message
            })
        }
    } catch (error) {
        console.error("Error:", error);
        swal.fire ({
            icon: 'error',
            title: 'Cuenta no creada',
            text: error
        })
    }
};

const login = async (username, password) => {
    const headers = {
        "Content-Type": "application/json",
    };

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({ username, password }), 
        });
        return response;
    } catch (error) {
        console.error("Error:", error);
    }
};

function run_app() {
    const register_button = document.getElementById('register-form');
    register_button.addEventListener('submit', register);
}

document.addEventListener('DOMContentLoaded', run_app);