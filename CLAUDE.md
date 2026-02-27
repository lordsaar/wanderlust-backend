# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI backend for Wanderlust — an AI travel story generator. Accepts trip parameters, calls the Anthropic Claude API, persists generated stories to PostgreSQL, and exposes a REST API consumed by a Next.js frontend.

## Development Commands

All development runs inside Docker. Start services with:
```bash
docker compose up --build
```

Then exec into the backend container for any other commands:
```bash
docker compose exec backend pytest tests/ -v --cov=app --cov-report=term-missing   # run all tests (80% coverage required)
docker compose exec backend pytest tests/test_stories.py::test_health_check -v      # run a single test
docker compose exec backend ruff check app/                                          # lint
docker compose exec backend mypy app/ --ignore-missing-imports                       # type check
docker compose exec backend alembic upgrade head                                     # apply migrations
docker compose exec backend alembic revision --autogenerate -m "description"        # generate a new migration
```

## Architecture

```
app/
  main.py              # FastAPI app, CORS config, router registration
  core/
    config.py          # Pydantic Settings (reads ANTHROPIC_API_KEY, DATABASE_URL from env/.env)
    database.py        # SQLAlchemy engine, SessionLocal, get_db() dependency
  models/
    story.py           # Story ORM model + DeclarativeBase (Base lives here, not a separate file)
  api/routes/
    stories.py         # All story endpoints + Pydantic request/response schemas (StoryRequest, StoryResponse)
  services/
    claude_service.py  # generate_story() — calls Anthropic API with claude-opus-4-6
alembic/
  env.py               # Imports Base from app.models.story; DATABASE_URL from settings
  versions/            # Migration files
tests/
  test_stories.py      # FastAPI TestClient tests; Claude API is mocked via unittest.mock.patch
```

## Key Architectural Notes

- **Pydantic schemas are co-located with routes** in `app/api/routes/stories.py`, not in a separate `schemas/` directory.
- **`DeclarativeBase` lives in `app/models/story.py`**. Any new models must import `Base` from there and be imported in `alembic/env.py` so Alembic detects them.
- **`generate_story()` in `claude_service.py` uses the synchronous Anthropic client** but is called with `await` from the async route handler. This works (Python treats it as a coroutine-compatible call) but is not truly async.
- **Tests mock the Claude API** at `app.api.routes.stories.generate_story` to avoid real API calls. Tests also use a real PostgreSQL database — the `DATABASE_URL` env var must point to a live Postgres instance when running tests.
- **CI gate**: 80% test coverage is enforced (`--cov-fail-under=80`). Deployments to Cloud Run only trigger on pushes to `main`.

## Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Required for story generation |
| `DATABASE_URL` | PostgreSQL connection string (defaults to `postgresql://wanderlust:wanderlust@db:5432/wanderlust`) |
