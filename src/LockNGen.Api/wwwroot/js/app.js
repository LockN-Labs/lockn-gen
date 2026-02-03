/**
 * Toast notification system
 */
const Toast = {
    container: null,

    init() {
        this.container = document.getElementById('toasts');
    },

    /**
     * Show a toast notification
     */
    show(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.container.appendChild(toast);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
};

/**
 * Application initialization
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    Toast.init();
    Modal.init();
    
    // Create gallery and form
    window.gallery = new Gallery('gallery');
    window.form = new Form('generation-form', window.gallery);
    
    // Load initial gallery content
    window.gallery.load();
    
    // Start polling for any existing processing items
    window.gallery.startPolling();
});
