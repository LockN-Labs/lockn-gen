/**
 * Modal component for generation details
 */
const Modal = {
    element: null,
    currentId: null,

    init() {
        this.element = document.getElementById('modal');
        this.backdrop = this.element.querySelector('.modal-backdrop');
        this.closeBtn = this.element.querySelector('.modal-close');
        this.cancelBtn = document.getElementById('modal-cancel');

        this.backdrop.addEventListener('click', () => this.hide());
        this.closeBtn.addEventListener('click', () => this.hide());
        this.cancelBtn.addEventListener('click', () => this.handleCancel());

        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && !this.element.hidden) {
                this.hide();
            }
        });
    },

    /**
     * Show modal with generation details
     */
    async show(id) {
        this.currentId = id;
        const gen = await API.getGeneration(id);
        
        if (!gen) {
            Toast.show('Generation not found', 'error');
            return;
        }

        // Populate modal content
        const img = document.getElementById('modal-img');
        if (gen.status === 'Completed') {
            img.src = API.getImageUrl(id);
            img.hidden = false;
        } else {
            img.hidden = true;
        }

        document.getElementById('modal-prompt').textContent = gen.prompt;
        
        const statusBadge = document.getElementById('modal-status');
        statusBadge.textContent = gen.status;
        statusBadge.className = `badge ${gen.status.toLowerCase()}`;

        document.getElementById('modal-duration').textContent = 
            gen.durationMs ? `${(gen.durationMs / 1000).toFixed(1)}s` : '';

        document.getElementById('modal-model').textContent = gen.model || '-';
        document.getElementById('modal-size').textContent = 
            gen.width && gen.height ? `${gen.width}×${gen.height}` : '-';
        document.getElementById('modal-steps').textContent = gen.steps || '-';
        document.getElementById('modal-guidance').textContent = gen.guidance || '-';
        document.getElementById('modal-seed').textContent = gen.seed || 'Random';

        // Download link
        const downloadLink = document.getElementById('modal-download');
        if (gen.status === 'Completed') {
            downloadLink.href = API.getImageUrl(id);
            downloadLink.download = `lockn-gen-${id}.png`;
            downloadLink.hidden = false;
        } else {
            downloadLink.hidden = true;
        }

        // Cancel button
        this.cancelBtn.hidden = gen.status !== 'Queued';

        this.element.hidden = false;
        document.body.style.overflow = 'hidden';
    },

    /**
     * Hide modal
     */
    hide() {
        this.element.hidden = true;
        this.currentId = null;
        document.body.style.overflow = '';
    },

    /**
     * Handle cancel button click
     */
    async handleCancel() {
        if (!this.currentId) return;

        try {
            const success = await API.cancelGeneration(this.currentId);
            if (success) {
                Toast.show('Generation cancelled', 'success');
                this.hide();
                // Refresh the gallery item
                const gen = await API.getGeneration(this.currentId);
                if (gen) window.gallery?.update(gen);
            } else {
                Toast.show('Could not cancel generation', 'error');
            }
        } catch (err) {
            Toast.show('Failed to cancel', 'error');
        }
    }
};
