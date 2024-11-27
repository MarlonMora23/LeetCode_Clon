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
                icon: 'question',
                title: '¿Deseas cerrar la sesión?',
                showCancelButton: true,
                confirmButtonText: 'Aceptar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Cierre de sesión exitoso',
                        showConfirmButton: false,
                        timer: 1000
                    }).then(() => {
                        window.location.href = currentUrl;
                    })
                }
            });

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

const search_problems = () => {
    const searchInput = document.getElementById('search-input');
    const difficultyFilter = document.getElementById('difficulty-filter');
    const statusFilter = document.getElementById('status-filter');
    const problemsContainer = document.getElementById('problems-container');
    const problemCards = problemsContainer.querySelectorAll('.problem-card');

    // Search functionality
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        filterProblems(); 
    });

    // Difficulty filter
    difficultyFilter.addEventListener('change', () => {
        const difficulty = difficultyFilter.value;
        difficultyFilter.setAttribute('data-selected', difficulty); 
        filterProblems(); 
    });

    // Status filter
    statusFilter.addEventListener('change', () => {
        const status = statusFilter.value;
        statusFilter.setAttribute('data-selected', status); 
        filterProblems(); 
    });

    // Filter problems based on search, difficulty, and status
    function filterProblems() {
        const query = searchInput.value.toLowerCase(); 
        const selectedDifficulty = difficultyFilter.getAttribute('data-selected').toLowerCase();
        const selectedStatus = statusFilter.getAttribute('data-selected').toLowerCase(); 

        problemCards.forEach(card => {
            const problemName = card.getAttribute('data-name').toLowerCase(); 
            const problemDifficulty = card.getAttribute('data-difficulty').toLowerCase(); 
            const problemStatus = card.getAttribute('data-status').toLowerCase(); 

            const matchesSearch = problemName.includes(query);
            const matchesDifficulty = selectedDifficulty === 'all' || problemDifficulty.includes(selectedDifficulty);
            const matchesStatus = selectedStatus === 'all' || problemStatus === selectedStatus;

            if (matchesSearch && matchesDifficulty && matchesStatus) {
                card.style.display = ''; // Show the problem card
            } else {
                card.style.display = 'none'; // Hide the problem card
            }
        });
    }
}


function run_app() {
    const logout_button = document.getElementById('logout-button');
    logout_button.addEventListener('click', logout);

    search_problems();
}

document.addEventListener('DOMContentLoaded', run_app);
