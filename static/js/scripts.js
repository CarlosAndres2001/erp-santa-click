// Contador animado para stats
document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.stat-number');

    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        let count = 0;
        const increment = target / 200;

        function updateCounter() {
            count += increment;
            if (count < target) {
                counter.textContent = Math.ceil(count);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        }
        updateCounter();
    });
});

// Mostrar/Ocultar "Enviando..." en botón contacto (simulación)
const contactForm = document.getElementById('contactForm');
const btnSubmit = contactForm.querySelector('button[type="submit"]');
const loadingSpan = btnSubmit.querySelector('.loading');
const buttonTextSpan = btnSubmit.querySelector('.button-text');

btnSubmit.addEventListener('click', () => {
    // Simular envío sin hacer nada
    loadingSpan.classList.add('show');
    buttonTextSpan.style.display = 'none';

    setTimeout(() => {
        loadingSpan.classList.remove('show');
        buttonTextSpan.style.display = 'inline';
        alert('Formulario de contacto simulado: no se envió nada realmente.');
        contactForm.reset();
    }, 1500);
});

// Simulación botón registro modal
const btnRegister = document.getElementById('btnRegister');
const registerForm = document.getElementById('registerForm');
const registerAlert = document.getElementById('registerAlert');

btnRegister.addEventListener('click', () => {
    // Mostrar "registrando..." y luego limpiar
    btnRegister.querySelector('.loading').classList.add('show');
    btnRegister.querySelector('.button-text').style.display = 'none';

    setTimeout(() => {
        btnRegister.querySelector('.loading').classList.remove('show');
        btnRegister.querySelector('.button-text').style.display = 'inline';
        registerAlert.innerHTML =
            '<div class="alert alert-success" role="alert">Registro simulado con éxito. (No se envió nada)</div>';
        registerForm.reset();
    }, 1500);
});
