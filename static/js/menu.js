// ============================
// Toggle Sidebar CON localStorage
// ============================

const toggleSidebar = document.getElementById('menu-toggle');
const sidebar = document.getElementById('sidebar');
const mainContent = document.querySelector('.main-content');

// ============================
// FUNCIÓN: Cargar estado guardado
// ============================
function loadSavedState() {
    // Cargar estado del sidebar
    const sidebarState = localStorage.getItem('sidebarCollapsed');
    const themeState = localStorage.getItem('themeMode');
    
    // Aplicar estado del sidebar
    if (sidebarState === 'true') {
        sidebar.classList.add('collapsed');
        document.body.classList.add('sidebar-collapsed');
        mainContent.classList.add('expanded');
    } else {
        sidebar.classList.remove('collapsed');
        document.body.classList.remove('sidebar-collapsed');
        mainContent.classList.remove('expanded');
    }
    
    // Aplicar estado del tema
    if (themeState === 'light') {
        document.body.classList.add('light-mode');
        themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        document.body.classList.remove('light-mode');
        themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
    }
}

// ============================
// FUNCIÓN: Guardar estado
// ============================
function saveSidebarState() {
    const isCollapsed = sidebar.classList.contains('collapsed');
    localStorage.setItem('sidebarCollapsed', isCollapsed);
}

function saveThemeState() {
    const isLight = document.body.classList.contains('light-mode');
    localStorage.setItem('themeMode', isLight ? 'light' : 'dark');
}

// ============================
// TOGGLE SIDEBAR
// ============================
toggleSidebar.addEventListener('click', () => {
    if (window.innerWidth <= 992) {
        sidebar.classList.toggle('show');
    } else {
        sidebar.classList.toggle('collapsed');
        document.body.classList.toggle('sidebar-collapsed');
        mainContent.classList.toggle('expanded');
        saveSidebarState();
        
        // Forzar actualización de tooltips
        window.dispatchEvent(new Event('resize'));
    }
});

// ============================
// THEME TOGGLE
// ============================
const themeToggleBtn = document.createElement('button');
themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
themeToggleBtn.classList.add('theme-toggle-btn');
themeToggleBtn.setAttribute('aria-label', 'Cambiar tema');
document.querySelector('.topbar-info').prepend(themeToggleBtn);

themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    
    if (document.body.classList.contains('light-mode')) {
        themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
    }
    
    saveThemeState();
});

// ============================
// CARGAR ESTADO AL INICIAR
// ============================
document.addEventListener('DOMContentLoaded', function() {
    loadSavedState();
    
    // También guardar estado cuando se redimensiona la ventana
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            if (sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
            }
        }
    });
});

// ============================
// MODAL LOGOUT MEJORADO
// ============================
const logoutBtn = document.querySelector('.logout-btn');
const modal = document.getElementById('logoutModal');
const cancelLogout = document.getElementById('cancelLogout');

if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (modal) {
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
        }
    });
}

if (cancelLogout) {
    cancelLogout.addEventListener('click', () => {
        if (modal) {
            modal.style.display = 'none';
        }
    });
}

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
        modal.style.display = 'none';
    }
});

console.log('✅ Sistema cargado correctamente');
console.log('📌 Sidebar estado:', localStorage.getItem('sidebarCollapsed'));
console.log('🎨 Tema estado:', localStorage.getItem('themeMode'));