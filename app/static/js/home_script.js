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
    const noResultsMessage = document.getElementById('no-results-message');

    // Add event listeners to all filters
    searchInput.addEventListener('input', filterProblems);
    difficultyFilter.addEventListener('change', filterProblems);
    statusFilter.addEventListener('change', filterProblems);

    // Filter problems based on search, difficulty, and status
    function filterProblems() {
        const query = searchInput.value
            .toLowerCase()
            .normalize("NFD") // Descompone caracteres diacríticos
            .replace(/[\u0300-\u036f]/g, ""); // Elimina diacríticos
        const selectedDifficulty = difficultyFilter.value.toLowerCase();
        const selectedStatus = statusFilter.value.toLowerCase();

        let visibleCount = 0;

        problemCards.forEach(card => {
            const problemName = card.getAttribute('data-name').toLowerCase();
            const normalizedProblemName = problemName
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "");
            const problemDifficulty = card.getAttribute('data-difficulty').toLowerCase();
            const problemStatus = card.getAttribute('data-status').toLowerCase();

            const matchesSearch = normalizedProblemName.includes(query);
            const matchesDifficulty = selectedDifficulty === 'all' || problemDifficulty.includes(selectedDifficulty);
            const matchesStatus = selectedStatus === 'all' || problemStatus === selectedStatus;

            if (matchesSearch && matchesDifficulty && matchesStatus) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Show or hide the "no results" message
        if (visibleCount === 0) {
            noResultsMessage.style.display = 'block';
        } else {
            noResultsMessage.style.display = 'none';
        }
    }
};


function run_app() {
    const logout_button = document.getElementById('logout-button');
    logout_button.addEventListener('click', logout);

    search_problems();
}

document.addEventListener('DOMContentLoaded', run_app);
