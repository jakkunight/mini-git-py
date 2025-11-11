/**
 * Mini Git PyUI - JavaScript principal
 * Maneja las interacciones de la interfaz, modales, AJAX y funcionalidades dinámicas
 */

// ===== VARIABLES GLOBALES =====
let currentRepository = null;
let toastTimeout = null;

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('🚀 Inicializando Mini Git PyUI...');
    
    // Inicializar componentes
    initializeModals();
    initializeToasts();
    initializeFormsValidation();
    initializeKeyboardShortcuts();
    
    // Event listeners globales
    setupGlobalEventListeners();
    
    console.log('✅ Mini Git PyUI inicializado correctamente');
}

// ===== MODALES =====
function initializeModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        // Cerrar modal al hacer clic en el overlay
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal(modal);
            }
        });
        
        // Cerrar modal con el botón X
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => closeModal(modal));
        }
    });
    
    // Event listeners específicos de modales
    setupModalEventListeners();
}

function setupModalEventListeners() {
    // Modal de clonar repositorio
    const cloneBtn = document.getElementById('cloneRepoBtn');
    const cloneModal = document.getElementById('cloneModal');
    const cloneForm = document.getElementById('cloneForm');
    
    if (cloneBtn && cloneModal) {
        cloneBtn.addEventListener('click', () => openModal(cloneModal));
    }
    
    if (cloneForm) {
        cloneForm.addEventListener('submit', handleCloneRepository);
    }
    
    // Modal de crear repositorio
    const createBtn = document.getElementById('createRepoBtn');
    const createModal = document.getElementById('createModal');
    const createForm = document.getElementById('createForm');
    
    if (createBtn && createModal) {
        createBtn.addEventListener('click', () => openModal(createModal));
    }
    
    if (createForm) {
        createForm.addEventListener('submit', handleCreateRepository);
    }
    
    // Botones de cancelar
    const cancelBtns = document.querySelectorAll('#cancelClone, #cancelCreate');
    cancelBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            closeModal(modal);
        });
    });
    
    // Botones de examinar carpetas
    const browseBtns = document.querySelectorAll('#browseLocalPath, #browseRepoPath');
    browseBtns.forEach(btn => {
        btn.addEventListener('click', handleBrowsePath);
    });
}

function openModal(modal) {
    if (!modal) return;
    
    modal.classList.add('show');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Focus en el primer input
    const firstInput = modal.querySelector('input, textarea, select');
    if (firstInput) {
        setTimeout(() => firstInput.focus(), 100);
    }
}

function closeModal(modal) {
    if (!modal) return;
    
    modal.classList.remove('show');
    modal.style.display = 'none';
    document.body.style.overflow = '';
    
    // Limpiar formularios
    const form = modal.querySelector('form');
    if (form) {
        form.reset();
    }
}

// ===== TOAST NOTIFICATIONS =====
function initializeToasts() {
    const toast = document.getElementById('toast');
    const toastClose = document.getElementById('toastClose');
    
    if (toastClose) {
        toastClose.addEventListener('click', hideToast);
    }
}

function showToast(message, type = 'info', duration = 5000) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    if (!toast || !toastMessage) return;
    
    // Limpiar timeout anterior
    if (toastTimeout) {
        clearTimeout(toastTimeout);
    }
    
    // Configurar mensaje y estilo
    toastMessage.textContent = message;
    toast.className = `toast show toast-${type}`;
    
    // Auto-ocultar después del duration
    toastTimeout = setTimeout(() => {
        hideToast();
    }, duration);
}

function hideToast() {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.classList.remove('show');
    }
    
    if (toastTimeout) {
        clearTimeout(toastTimeout);
        toastTimeout = null;
    }
}

// ===== VALIDACIÓN DE FORMULARIOS =====
function initializeFormsValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => validateField(input));
            input.addEventListener('input', () => clearFieldError(input));
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const isValid = field.checkValidity() && value.length > 0;
    
    if (!isValid) {
        showFieldError(field, getFieldErrorMessage(field));
        return false;
    }
    
    clearFieldError(field);
    return true;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('field-error');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error-message';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('field-error');
    
    const existingError = field.parentNode.querySelector('.field-error-message');
    if (existingError) {
        existingError.remove();
    }
}

function getFieldErrorMessage(field) {
    const fieldName = field.getAttribute('placeholder') || field.name || 'Este campo';
    
    if (field.type === 'email') {
        return 'Por favor, ingresa un email válido';
    }
    
    if (field.type === 'url') {
        return 'Por favor, ingresa una URL válida';
    }
    
    return `${fieldName} es requerido`;
}

// ===== ATAJOS DE TECLADO =====
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Esc para cerrar modales
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                closeModal(openModal);
                return;
            }
            
            // Cerrar toast
            hideToast();
        }
        
        // Ctrl/Cmd + K para buscar
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('commitSearch') || 
                               document.getElementById('globalSearch');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Ctrl/Cmd + N para nuevo repositorio
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            const createBtn = document.getElementById('createRepoBtn');
            if (createBtn) {
                createBtn.click();
            }
        }
        
        // Ctrl/Cmd + Shift + K para clonar
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'K') {
            e.preventDefault();
            const cloneBtn = document.getElementById('cloneRepoBtn');
            if (cloneBtn) {
                cloneBtn.click();
            }
        }
    });
}

// ===== EVENT LISTENERS GLOBALES =====
function setupGlobalEventListeners() {
    // Actualizar repositorios en el sidebar
    const refreshBtn = document.getElementById('refreshRepos');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshRepositoriesList);
    }
    
    // Enlaces de navegación
    setupNavigationLinks();
    
    // Botones de acción en cards
    setupActionButtons();
}

function setupNavigationLinks() {
    // Interceptar enlaces internos para SPA-like behavior
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href^="/"]');
        if (link && !link.hasAttribute('download') && !link.target) {
            // Podrías implementar navegación SPA aquí si lo deseas
            // Por ahora, usar navegación normal
        }
    });
}

function setupActionButtons() {
    // Copiar SHA de commits
    document.addEventListener('click', function(e) {
        const copyBtn = e.target.closest('[data-copy]');
        if (copyBtn) {
            const textToCopy = copyBtn.dataset.copy;
            copyToClipboard(textToCopy);
        }
    });
}

// ===== MANEJO DE REPOSITORIOS =====
async function handleCloneRepository(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const repoUrl = formData.get('repo_url');
    const localPath = formData.get('local_path');
    
    // Validar campos
    if (!repoUrl || !localPath) {
        showToast('Todos los campos son requeridos', 'error');
        return;
    }
    
    // Mostrar loading
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="bi bi-arrow-clockwise spin"></i> Clonando...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/clone', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showToast(result.message, 'success');
            closeModal(document.getElementById('cloneModal'));
            
            // Actualizar lista de repositorios
            setTimeout(() => {
                refreshRepositoriesList();
            }, 1000);
            
        } else {
            showToast(result.message || 'Error clonando repositorio', 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión', 'error');
    } finally {
        // Restaurar botón
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

async function handleCreateRepository(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const repoName = formData.get('repo_name');
    const repoPath = formData.get('repo_path');
    
    // Validar campos
    if (!repoName || !repoPath) {
        showToast('Todos los campos son requeridos', 'error');
        return;
    }
    
    // Validar nombre del repositorio
    if (!/^[a-zA-Z0-9._-]+$/.test(repoName)) {
        showToast('El nombre del repositorio solo puede contener letras, números, puntos, guiones y guiones bajos', 'error');
        return;
    }
    
    // Mostrar loading
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="bi bi-arrow-clockwise spin"></i> Creando...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/create-repo', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showToast(result.message, 'success');
            closeModal(document.getElementById('createModal'));
            
            // Redirigir al nuevo repositorio
            setTimeout(() => {
                window.location.href = `/repository/${encodeURIComponent(result.path)}`;
            }, 1500);
            
        } else {
            showToast(result.message || 'Error creando repositorio', 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión', 'error');
    } finally {
        // Restaurar botón
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

async function refreshRepositoriesList() {
    const refreshBtn = document.getElementById('refreshRepos');
    if (refreshBtn) {
        const icon = refreshBtn.querySelector('i');
        icon.classList.add('spin');
    }
    
    try {
        const response = await fetch('/api/repositories');
        const data = await response.json();
        
        if (data.status === 'success') {
            updateRepositoriesSidebar(data.data);
            showToast('Repositorios actualizados', 'success', 2000);
        } else {
            showToast('Error actualizando repositorios', 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión', 'error');
    } finally {
        if (refreshBtn) {
            const icon = refreshBtn.querySelector('i');
            icon.classList.remove('spin');
        }
    }
}

function updateRepositoriesSidebar(repositories) {
    const sidebarList = document.getElementById('repositories-list');
    if (!sidebarList) return;
    
    sidebarList.innerHTML = '';
    
    if (repositories.length === 0) {
        sidebarList.innerHTML = `
            <div class="sidebar-empty">
                <p>No hay repositorios</p>
            </div>
        `;
        return;
    }
    
    repositories.forEach(repo => {
        const repoElement = createRepositoryElement(repo);
        sidebarList.appendChild(repoElement);
    });
}

function createRepositoryElement(repo) {
    const element = document.createElement('div');
    element.className = 'sidebar-repo-item';
    element.innerHTML = `
        <div class="sidebar-repo-icon">
            <i class="bi bi-${repo.type === 'mini-git' ? 'git' : 'github'}"></i>
        </div>
        <div class="sidebar-repo-info">
            <div class="sidebar-repo-name">${escapeHtml(repo.name)}</div>
            <div class="sidebar-repo-type">${repo.type}</div>
        </div>
    `;
    
    element.addEventListener('click', () => {
        window.location.href = `/repository/${encodeURIComponent(repo.path)}`;
    });
    
    return element;
}

// ===== UTILIDADES =====
function handleBrowsePath(e) {
    // En un entorno real, esto abriría un diálogo de selección de carpeta
    // Por ahora, mostrar un placeholder
    showToast('Funcionalidad de explorar carpetas en desarrollo', 'info');
}

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copiado al portapapeles', 'success', 2000);
    } catch (error) {
        console.error('Error copiando al portapapeles:', error);
        
        // Fallback para navegadores antiguos
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            showToast('Copiado al portapapeles', 'success', 2000);
        } catch (fallbackError) {
            showToast('No se pudo copiar al portapapeles', 'error');
        }
        
        document.body.removeChild(textArea);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
        return 'hace 1 día';
    } else if (diffDays < 7) {
        return `hace ${diffDays} días`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `hace ${weeks} semana${weeks > 1 ? 's' : ''}`;
    } else {
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== FUNCIONES ESPECÍFICAS DE PÁGINA =====

// Funciones para la página de repositorio
if (window.location.pathname.includes('/repository/')) {
    document.addEventListener('DOMContentLoaded', function() {
        initializeRepositoryPage();
    });
}

function initializeRepositoryPage() {
    // Cargar estado del repositorio periódicamente
    setInterval(loadRepositoryStatus, 30000); // cada 30 segundos
    
    // Event listeners específicos del repositorio
    setupRepositoryEventListeners();
}

function setupRepositoryEventListeners() {
    // Tabs de navegación
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.addEventListener('click', handleTabClick);
    });
    
    // Selector de rama
    const branchSelector = document.getElementById('branchSelector');
    if (branchSelector) {
        branchSelector.addEventListener('click', showBranchSelector);
    }
}

function handleTabClick(e) {
    e.preventDefault();
    
    const targetTab = e.currentTarget.dataset.tab;
    if (!targetTab) return;
    
    // Actualizar tabs activos
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    e.currentTarget.classList.add('active');
    
    // Mostrar contenido correspondiente
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    
    const targetPane = document.getElementById(targetTab + '-content');
    if (targetPane) {
        targetPane.classList.add('active');
        
        // Cargar contenido específico si es necesario
        loadTabContent(targetTab);
    }
}

async function loadTabContent(tabName) {
    switch (tabName) {
        case 'history':
            await loadCommitHistory();
            break;
        case 'branches':
            await loadBranches();
            break;
        case 'files':
            await loadFileTree();
            break;
        default:
            break;
    }
}

async function loadRepositoryStatus() {
    const repoPath = getCurrentRepositoryPath();
    if (!repoPath) return;
    
    try {
        const response = await fetch(`/api/repository/${encodeURIComponent(repoPath)}/status`);
        const data = await response.json();
        
        if (data.status === 'success') {
            updateRepositoryStatus(data.data);
        }
    } catch (error) {
        console.error('Error cargando estado del repositorio:', error);
    }
}

function updateRepositoryStatus(status) {
    // Actualizar indicador de estado
    const statusIndicator = document.getElementById('repoStatus');
    if (statusIndicator) {
        const isClean = status.clean;
        statusIndicator.innerHTML = isClean ? 
            '<span class="status-indicator status-clean"><i class="bi bi-check-circle"></i> Limpio</span>' :
            '<span class="status-indicator status-dirty"><i class="bi bi-exclamation-circle"></i> Cambios pendientes</span>';
    }
    
    // Actualizar badge de cambios
    const changesBadge = document.getElementById('changesBadge');
    if (changesBadge) {
        const totalChanges = (status.modified_files?.length || 0) + 
                            (status.staged_files?.length || 0) + 
                            (status.untracked_files?.length || 0);
        
        changesBadge.textContent = totalChanges;
        changesBadge.style.display = totalChanges > 0 ? 'inline' : 'none';
    }
}

function getCurrentRepositoryPath() {
    const pathMatch = window.location.pathname.match(/\/repository\/(.+)$/);
    return pathMatch ? decodeURIComponent(pathMatch[1]) : null;
}

function showBranchSelector() {
    // Implementar selector de ramas
    showToast('Selector de ramas en desarrollo', 'info');
}

async function loadCommitHistory() {
    // Implementar carga de historial
    console.log('Cargando historial de commits...');
}

async function loadBranches() {
    // Implementar carga de ramas
    console.log('Cargando ramas...');
}

async function loadFileTree() {
    // Implementar árbol de archivos
    console.log('Cargando árbol de archivos...');
}

// ===== ESTILOS DINÁMICOS =====
const style = document.createElement('style');
style.textContent = `
    .field-error {
        border-color: var(--error-color) !important;
        box-shadow: 0 0 0 2px rgba(218, 54, 51, 0.2) !important;
    }
    
    .field-error-message {
        color: var(--error-color);
        font-size: var(--font-xs);
        margin-top: var(--space-1);
    }
    
    .spin {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .toast-success {
        border-left: 4px solid var(--success-color);
    }
    
    .toast-error {
        border-left: 4px solid var(--error-color);
    }
    
    .toast-warning {
        border-left: 4px solid var(--warning-color);
    }
    
    .toast-info {
        border-left: 4px solid var(--info-color);
    }
    
    .sidebar-empty {
        text-align: center;
        padding: var(--space-6);
        color: var(--text-muted);
        font-size: var(--font-sm);
    }
`;
document.head.appendChild(style);

// ===== EXPORT PARA TESTING =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showToast,
        hideToast,
        copyToClipboard,
        formatFileSize,
        formatDate,
        debounce,
        escapeHtml
    };
}