# Wanderlust Backend

FastAPI backend for the Wanderlust AI Travel Story Generator.

## Tech Stack

- **Python 3.12** / FastAPI
- **PostgreSQL** with SQLAlchemy ORM
- **Alembic** for database migrations
- **Anthropic Claude API** for AI story generation
- **Docker** for local development
- **Google Cloud Run** for production deployment
- **Google Cloud SQL** for production database
- **Google Secret Manager** for secrets

## Architecture
```
Frontend (Next.js) → Backend (FastAPI) → Claude API
                            ↓
                      PostgreSQL (Cloud SQL)
```

## Local Development

### Prerequisites
- Docker Desktop
- Python 3.12+

### Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your API key:
```bash
cp .env.example .env
```

3. Start the services:
```bash
docker compose up --build
```

4. API is available at `http://localhost:8000`
5. Interactive docs at `http://localhost:8000/docs`

### Running Tests
```bash
docker compose exec backend pytest tests/ -v --cov=app --cov-report=term-missing
```

### Code Quality
```bash
docker compose exec backend ruff check app/      # linting
docker compose exec backend mypy app/            # type checking
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check with uptime |
| POST | `/api/stories/generate` | Generate a new story |
| GET | `/api/stories/` | List all stories |
| DELETE | `/api/stories/{id}` | Delete a story |

## CI/CD Pipeline

Every push to `main` triggers:
1. Ruff linting
2. Mypy type checking
3. Pytest with 80% coverage gate
4. Docker build and push to Artifact Registry
5. Automatic deployment to Cloud Run

## Production

- **API:** https://wanderlust-backend-wot5c6gzla-ew.a.run.app
- **Docs:** https://wanderlust-backend-wot5c6gzla-ew.a.run.app/docs
