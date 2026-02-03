/**
 * Gallery component for displaying generations
 */
class Gallery {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.loadingEl = document.getElementById('loading');
        this.emptyEl = document.getElementById('empty');
        this.page = 1;
        this.pageSize = 20;
        this.loading = false;
        this.hasMore = true;
        this.items = new Map();
        this.pollInterval = null;
        
        this.setupInfiniteScroll();
    }

    /**
     * Load the next page of generations
     */
    async load() {
        if (this.loading || !this.hasMore) return;
        
        this.loading = true;
        this.showLoading(true);

        try {
            const data = await API.getGenerations(this.page, this.pageSize);
            
            if (data.items.length === 0 && this.page === 1) {
                this.showEmpty(true);
            } else {
                this.showEmpty(false);
                this.render(data.items);
                this.hasMore = this.page < data.totalPages;
                this.page++;
            }
        } catch (err) {
            Toast.show('Failed to load gallery', 'error');
        } finally {
            this.loading = false;
            this.showLoading(false);
        }
    }

    /**
     * Render items to the gallery
     */
    render(items) {
        items.forEach(item => {
            if (this.items.has(item.id)) return;
            
            const card = this.createCard(item);
            this.container.appendChild(card);
            this.items.set(item.id, item);
        });
    }

    /**
     * Create a gallery card element
     */
    createCard(item) {
        const card = document.createElement('div');
        card.className = `card status-${item.status.toLowerCase()}`;
        card.dataset.id = item.id;

        if (item.status === 'Completed') {
            const img = document.createElement('img');
            img.src = API.getImageUrl(item.id);
            img.alt = item.prompt;
            img.loading = 'lazy';
            card.appendChild(img);
        } else {
            const badge = document.createElement('div');
            badge.className = 'status-badge';
            badge.textContent = item.status;
            card.appendChild(badge);
        }

        card.addEventListener('click', () => Modal.show(item.id));
        return card;
    }

    /**
     * Add a new item to the beginning of the gallery
     */
    prepend(item) {
        if (this.items.has(item.id)) return;
        
        this.showEmpty(false);
        const card = this.createCard(item);
        this.container.insertBefore(card, this.container.firstChild);
        this.items.set(item.id, item);
    }

    /**
     * Update an existing item
     */
    update(item) {
        const card = this.container.querySelector(`[data-id="${item.id}"]`);
        if (!card) return;

        card.className = `card status-${item.status.toLowerCase()}`;
        card.innerHTML = '';

        if (item.status === 'Completed') {
            const img = document.createElement('img');
            img.src = API.getImageUrl(item.id);
            img.alt = item.prompt;
            card.appendChild(img);
        } else {
            const badge = document.createElement('div');
            badge.className = 'status-badge';
            badge.textContent = item.status;
            card.appendChild(badge);
        }

        this.items.set(item.id, item);
    }

    /**
     * Setup infinite scroll
     */
    setupInfiniteScroll() {
        const observer = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) {
                this.load();
            }
        }, { rootMargin: '100px' });

        observer.observe(this.loadingEl);
    }

    /**
     * Start polling for updates on processing items
     */
    startPolling() {
        if (this.pollInterval) return;
        
        this.pollInterval = setInterval(() => this.pollUpdates(), 5000);
    }

    /**
     * Stop polling
     */
    stopPolling() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }

    /**
     * Poll for updates on non-terminal items
     */
    async pollUpdates() {
        const processing = [...this.items.values()].filter(
            item => item.status === 'Queued' || item.status === 'Processing'
        );

        for (const item of processing) {
            try {
                const updated = await API.getGeneration(item.id);
                if (updated && updated.status !== item.status) {
                    this.update(updated);
                    
                    if (updated.status === 'Completed') {
                        Toast.show('Generation completed!', 'success');
                    } else if (updated.status === 'Failed') {
                        Toast.show('Generation failed', 'error');
                    }
                }
            } catch (err) {
                // Ignore polling errors
            }
        }
    }

    showLoading(show) {
        this.loadingEl.hidden = !show;
    }

    showEmpty(show) {
        this.emptyEl.hidden = !show;
    }
}
