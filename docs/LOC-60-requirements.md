# LOC-60: Frontend Gallery UI

## Overview
Create a simple web-based gallery UI for viewing and managing image generations. The UI will be served directly from the .NET API using static files.

## Functional Requirements

### FR-1: Gallery View
- Display grid of generated images (thumbnails)
- Show generation status indicator (queued, processing, completed, failed)
- Infinite scroll or pagination for large collections
- Click image to view full size

### FR-2: Generation Form
- Text input for prompt (multiline)
- Optional negative prompt field
- Model/workflow selector dropdown
- Advanced settings collapsible panel:
  - Steps slider (1-100, default 20)
  - Guidance slider (0-30, default 7.5)
  - Width/Height inputs (64-2048, step 64)
  - Seed input (optional)
- Submit button with loading state

### FR-3: Generation Detail View
- Full-size image display
- Generation metadata (prompt, settings, duration)
- Download button
- Delete/Cancel button
- Status badge with progress (if processing)

### FR-4: Real-time Updates
- Auto-refresh gallery when generations complete
- Show processing progress indicator
- Toast notifications for completion/failure

## Non-Functional Requirements

### NFR-1: Technology Stack
- Vanilla HTML/CSS/JavaScript (no framework required)
- Responsive design (mobile-friendly)
- Dark mode support (prefers-color-scheme)

### NFR-2: Performance
- Lazy load images
- Thumbnail generation (separate from full image)
- Debounced form inputs

### NFR-3: Accessibility
- Semantic HTML
- ARIA labels for interactive elements
- Keyboard navigation support

## Technical Notes
- Serve from wwwroot/ directory in API project
- Use fetch() for API calls to /api/generations
- Poll /api/generations/{id} for status updates (5s interval)
- Consider WebSocket for real-time updates (future enhancement)

## File Structure
```
src/LockNGen.Api/wwwroot/
├── index.html          # Main gallery page
├── css/
│   └── styles.css      # All styles
└── js/
    ├── api.js          # API client wrapper
    ├── gallery.js      # Gallery component
    ├── form.js         # Generation form
    └── app.js          # Main app initialization
```
