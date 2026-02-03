# LOC-59: Text-to-Image API Endpoints

## Overview
Expose REST API endpoints for text-to-image generation using the ComfyUI backend (LOC-58).

## Functional Requirements

### FR-1: Generation Request Endpoint
- POST `/api/generations` — Submit new generation request
- Request body:
  ```json
  {
    "prompt": "string (required)",
    "negativePrompt": "string (optional)",
    "model": "string (optional, default: sdxl)",
    "steps": "int (optional, default: 20)",
    "guidance": "float (optional, default: 7.5)",
    "width": "int (optional, default: 1024)",
    "height": "int (optional, default: 1024)",
    "seed": "int (optional, -1 for random)"
  }
  ```
- Response: Generation entity with ID and status

### FR-2: Generation Status Endpoint
- GET `/api/generations/{id}` — Get generation by ID
- Returns: Generation entity with current status, progress, metadata

### FR-3: List Generations Endpoint
- GET `/api/generations` — List generations with pagination
- Query params: `page`, `pageSize`, `status` filter
- Returns: Paginated list of generations

### FR-4: Cancel Generation Endpoint
- DELETE `/api/generations/{id}` — Cancel pending/processing generation
- Returns: 204 No Content on success

### FR-5: Get Generated Image Endpoint
- GET `/api/generations/{id}/image` — Stream the generated image
- Returns: Image bytes with appropriate Content-Type
- Returns 404 if not completed or failed

### FR-6: List Available Models
- GET `/api/models` — List available workflow templates
- Returns: Array of model identifiers (txt2img-sdxl, etc.)

## Non-Functional Requirements

### NFR-1: Input Validation
- Validate prompt length (max 2000 chars)
- Validate dimensions (min 64, max 2048, divisible by 64)
- Validate steps (1-100)
- Validate guidance (0.0-30.0)

### NFR-2: OpenAPI Documentation
- All endpoints documented with Swagger/OpenAPI
- Request/response examples included

### NFR-3: Error Handling
- Consistent error response format
- Appropriate HTTP status codes (400, 404, 500)

## Technical Notes
- Use IGenerationService from LOC-58
- Minimal API pattern (consistent with existing endpoints)
- Async/await throughout
