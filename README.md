# Wanderlust Backend

FastAPI backend for the Wanderlust AI Travel Story Generator.

## Local Development

1. Copy `.env.example` to `.env` and fill in your API key:
```bash
   cp .env.example .env
```

2. Start the services:
```bash
   docker compose up --build
```

3. API available at: http://localhost:8000
4. Docs available at: http://localhost:8000/docs

## Endpoints

- `GET /health` — health check
- `POST /api/stories/generate` — generate a travel story
# Quality gates added
