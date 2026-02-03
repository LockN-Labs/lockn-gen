# LOC-60: Frontend Gallery UI — Architecture

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        index.html                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Navigation  │  │ Gallery Grid │  │ Detail Modal │         │
│  └──────────────┘  └──────┬───────┘  └──────────────┘         │
│                           │                                    │
│  ┌──────────────┐         │                                    │
│  │ Create Form  │         │                                    │
│  └──────────────┘         ▼                                    │
│                    ┌──────────────┐                            │
│                    │  Gallery.js  │                            │
│                    └──────┬───────┘                            │
│                           │                                    │
│                    ┌──────▼───────┐                            │
│                    │    Api.js    │──────▶ /api/generations   │
│                    └──────────────┘                            │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## File Structure

```
src/LockNGen.Api/wwwroot/
├── index.html              # Single page app
├── css/
│   └── styles.css          # All styles (dark mode, responsive)
└── js/
    ├── api.js              # API client (fetch wrapper)
    ├── gallery.js          # Gallery grid + infinite scroll
    ├── form.js             # Generation form + validation
    ├── modal.js            # Detail view modal
    └── app.js              # Entry point, event wiring
```

## API Client (api.js)

```javascript
const API = {
    baseUrl: '/api',
    
    async createGeneration(data) {
        const res = await fetch(`${this.baseUrl}/generations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw await res.json();
        return res.json();
    },
    
    async getGenerations(page = 1, pageSize = 20) {
        const res = await fetch(
            `${this.baseUrl}/generations?page=${page}&pageSize=${pageSize}`
        );
        return res.json();
    },
    
    async getGeneration(id) {
        const res = await fetch(`${this.baseUrl}/generations/${id}`);
        if (!res.ok) return null;
        return res.json();
    },
    
    async cancelGeneration(id) {
        const res = await fetch(`${this.baseUrl}/generations/${id}`, {
            method: 'DELETE'
        });
        return res.ok;
    },
    
    async getModels() {
        const res = await fetch(`${this.baseUrl}/models`);
        return res.json();
    },
    
    getImageUrl(id) {
        return `${this.baseUrl}/generations/${id}/image`;
    }
};
```

## Gallery Component (gallery.js)

```javascript
class Gallery {
    constructor(container) {
        this.container = container;
        this.page = 1;
        this.loading = false;
        this.hasMore = true;
        this.pollInterval = null;
    }
    
    async load() {
        if (this.loading || !this.hasMore) return;
        this.loading = true;
        
        const data = await API.getGenerations(this.page);
        this.render(data.items);
        
        this.hasMore = this.page < data.totalPages;
        this.page++;
        this.loading = false;
    }
    
    render(items) {
        items.forEach(item => {
            const card = this.createCard(item);
            this.container.appendChild(card);
        });
    }
    
    createCard(item) {
        const card = document.createElement('div');
        card.className = `card status-${item.status.toLowerCase()}`;
        card.dataset.id = item.id;
        
        if (item.status === 'Completed') {
            const img = document.createElement('img');
            img.src = API.getImageUrl(item.id);
            img.loading = 'lazy';
            card.appendChild(img);
        } else {
            card.innerHTML = `<div class="status-badge">${item.status}</div>`;
        }
        
        card.addEventListener('click', () => Modal.show(item.id));
        return card;
    }
    
    startPolling() {
        this.pollInterval = setInterval(() => this.refresh(), 5000);
    }
    
    stopPolling() {
        clearInterval(this.pollInterval);
    }
}
```

## CSS Architecture

```css
/* Variables for theming */
:root {
    --bg-primary: #1a1a2e;
    --bg-secondary: #16213e;
    --text-primary: #eee;
    --accent: #4ecca3;
    --error: #e74c3c;
    --warning: #f39c12;
}

/* Responsive grid */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
}

/* Status indicators */
.card.status-queued { border: 2px dashed var(--warning); }
.card.status-processing { animation: pulse 2s infinite; }
.card.status-completed { border: 2px solid var(--accent); }
.card.status-failed { border: 2px solid var(--error); }
```

## Static File Serving (Program.cs)

```csharp
// Add after existing middleware
app.UseDefaultFiles();  // Serves index.html for /
app.UseStaticFiles();   // Serves wwwroot/
```

## Data Flow

1. **Page Load**
   - `app.js` initializes Gallery and Form
   - Gallery.load() fetches first page
   - Form populates model dropdown

2. **Create Generation**
   - User fills form, clicks submit
   - Form.submit() calls API.createGeneration()
   - On success: add card to gallery, start polling

3. **Poll for Updates**
   - Gallery checks processing generations every 5s
   - When status changes: update card, stop polling if terminal

4. **View Detail**
   - Click card opens Modal
   - Modal fetches full generation data
   - Displays full image + metadata

---

*Phase 2 Architecture — Created 2026-02-03*
