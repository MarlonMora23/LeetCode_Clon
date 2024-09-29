const logout = async (event) => {
    event.preventDefault();

    const currentUrl = window.location.href;

    try {
        const response = await fetch('/logout', {
            method: 'POST',
        });

        if (response.ok) {
            // Redirigir al home si la creación fue exitosa
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
    
function run_app() {
    const logout_button = document.getElementById('logout-button');
    logout_button.addEventListener('click', logout);
}

document.addEventListener('DOMContentLoaded', run_app);

