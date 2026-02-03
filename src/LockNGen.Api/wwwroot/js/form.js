/**
 * Generation form handler
 */
class Form {
    constructor(formId, gallery) {
        this.form = document.getElementById(formId);
        this.gallery = gallery;
        this.submitBtn = document.getElementById('submit-btn');
        this.btnText = this.submitBtn.querySelector('.btn-text');
        this.btnLoading = this.submitBtn.querySelector('.btn-loading');
        
        this.setupEventListeners();
        this.loadModels();
    }

    /**
     * Setup form event listeners
     */
    setupEventListeners() {
        this.form.addEventListener('submit', e => this.handleSubmit(e));
        
        // Update slider value displays
        const stepsSlider = document.getElementById('steps');
        const guidanceSlider = document.getElementById('guidance');
        
        stepsSlider.addEventListener('input', () => {
            document.getElementById('steps-value').textContent = stepsSlider.value;
        });
        
        guidanceSlider.addEventListener('input', () => {
            document.getElementById('guidance-value').textContent = guidanceSlider.value;
        });
    }

    /**
     * Load available models into dropdown
     */
    async loadModels() {
        try {
            const models = await API.getModels();
            const select = document.getElementById('model');
            select.innerHTML = '';
            
            models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model.replace('txt2img-', '').toUpperCase();
                select.appendChild(option);
            });
        } catch (err) {
            // Use default if API fails
        }
    }

    /**
     * Handle form submission
     */
    async handleSubmit(e) {
        e.preventDefault();
        
        if (this.submitBtn.disabled) return;

        const formData = new FormData(this.form);
        const data = {
            prompt: formData.get('prompt'),
            negativePrompt: formData.get('negativePrompt') || undefined,
            model: formData.get('model'),
            steps: parseInt(formData.get('steps')),
            guidance: parseFloat(formData.get('guidance')),
            width: parseInt(formData.get('width')),
            height: parseInt(formData.get('height')),
            seed: formData.get('seed') ? parseInt(formData.get('seed')) : -1
        };

        this.setLoading(true);

        try {
            const generation = await API.createGeneration(data);
            this.gallery.prepend(generation);
            this.gallery.startPolling();
            this.form.reset();
            document.getElementById('steps-value').textContent = '20';
            document.getElementById('guidance-value').textContent = '7.5';
            Toast.show('Generation queued!', 'success');
        } catch (err) {
            Toast.show(err.message, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Set loading state
     */
    setLoading(loading) {
        this.submitBtn.disabled = loading;
        this.btnText.hidden = loading;
        this.btnLoading.hidden = !loading;
    }
}
