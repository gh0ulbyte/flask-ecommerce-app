// JavaScript principal para la tienda online

// Funciones de utilidad
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Manejo de formularios
document.addEventListener('DOMContentLoaded', function() {
    // Validación de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '#bdc3c7';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Por favor completa todos los campos requeridos', 'error');
            }
        });
    });
    
    // Filtro de categorías en productos
    const categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const category = this.value;
            const url = new URL(window.location);
            if (category) {
                url.searchParams.set('category', category);
            } else {
                url.searchParams.delete('category');
            }
            window.location.href = url.toString();
        });
    }
    
    // Confirmación para acciones destructivas
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });
});

// Funciones para el carrito
function updateCartQuantity(itemId, quantity) {
    if (quantity <= 0) {
        if (confirm('¿Quieres eliminar este producto del carrito?')) {
            window.location.href = `/remove_from_cart/${itemId}`;
        }
        return;
    }
    
    // Aquí podrías implementar una actualización AJAX del carrito
    // Por ahora, recargamos la página
    window.location.href = `/update_cart/${itemId}/${quantity}`;
}

// Funciones para administración
function updateOrderStatus(orderId, status) {
    fetch(`/admin/orders/${orderId}/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({status: status})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Estado del pedido actualizado correctamente', 'success');
        } else {
            showAlert('Error al actualizar el estado del pedido', 'error');
        }
    })
    .catch(error => {
        showAlert('Error de conexión', 'error');
    });
}

// Funciones de carga de archivos
function uploadFile(formData) {
    return fetch('/admin/files/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json());
}

// Validación de imágenes
function validateImage(file) {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!allowedTypes.includes(file.type)) {
        showAlert('Tipo de archivo no permitido. Solo se permiten JPG, PNG y GIF.', 'error');
        return false;
    }
    
    if (file.size > maxSize) {
        showAlert('El archivo es demasiado grande. Máximo 16MB.', 'error');
        return false;
    }
    
    return true;
}

// Funciones de búsqueda
function searchProducts(query) {
    const url = new URL(window.location);
    url.searchParams.set('search', query);
    window.location.href = url.toString();
}

// Funciones de paginación
function goToPage(page) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}

// Funciones de ordenamiento
function sortProducts(sortBy) {
    const url = new URL(window.location);
    url.searchParams.set('sort', sortBy);
    window.location.href = url.toString();
}

// Funciones de filtros
function applyFilters() {
    const category = document.getElementById('category')?.value;
    const minPrice = document.getElementById('minPrice')?.value;
    const maxPrice = document.getElementById('maxPrice')?.value;
    
    const url = new URL(window.location);
    
    if (category) url.searchParams.set('category', category);
    else url.searchParams.delete('category');
    
    if (minPrice) url.searchParams.set('minPrice', minPrice);
    else url.searchParams.delete('minPrice');
    
    if (maxPrice) url.searchParams.set('maxPrice', maxPrice);
    else url.searchParams.delete('maxPrice');
    
    window.location.href = url.toString();
}

// Funciones de responsive
function toggleMobileMenu() {
    const nav = document.querySelector('.navbar-nav');
    nav.classList.toggle('mobile-open');
}

// Funciones de accesibilidad
function handleKeyboardNavigation(e) {
    if (e.key === 'Enter' || e.key === ' ') {
        e.target.click();
    }
}

// Event listeners globales
document.addEventListener('keydown', function(e) {
    // Escape para cerrar modales
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

// Funciones de notificaciones
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// CSS para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .mobile-open {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: #2c3e50;
        padding: 1rem;
    }
`;
document.head.appendChild(style);
