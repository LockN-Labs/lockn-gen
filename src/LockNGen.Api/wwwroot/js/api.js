/**
 * API client for LockN Gen
 */
const API = {
    baseUrl: '/api',

    /**
     * Create a new generation request
     */
    async createGeneration(data) {
        const res = await fetch(`${this.baseUrl}/generations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Failed to create generation');
        }
        return res.json();
    },

    /**
     * Get paginated list of generations
     */
    async getGenerations(page = 1, pageSize = 20) {
        const res = await fetch(
            `${this.baseUrl}/generations?page=${page}&pageSize=${pageSize}`
        );
        if (!res.ok) throw new Error('Failed to fetch generations');
        return res.json();
    },

    /**
     * Get a single generation by ID
     */
    async getGeneration(id) {
        const res = await fetch(`${this.baseUrl}/generations/${id}`);
        if (!res.ok) return null;
        return res.json();
    },

    /**
     * Cancel a queued generation
     */
    async cancelGeneration(id) {
        const res = await fetch(`${this.baseUrl}/generations/${id}`, {
            method: 'DELETE'
        });
        return res.ok;
    },

    /**
     * Get available models/workflows
     */
    async getModels() {
        const res = await fetch(`${this.baseUrl}/models`);
        if (!res.ok) return ['txt2img-sdxl'];
        return res.json();
    },

    /**
     * Get the image URL for a generation
     */
    getImageUrl(id) {
        return `${this.baseUrl}/generations/${id}/image`;
    }
};
