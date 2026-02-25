import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_health_check():
    """Health endpoint should return 200 and correct status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "wanderlust-backend"


def test_generate_story_missing_destination():
    """Should return 422 when destination is empty."""
    response = client.post("/api/stories/generate", json={
        "destination": "",
        "travel_style": "foodie",
        "duration_days": 3
    })
    assert response.status_code == 400


def test_generate_story_invalid_payload():
    """Should return 422 when required fields are missing."""
    response = client.post("/api/stories/generate", json={
        "travel_style": "foodie"
    })
    assert response.status_code == 422


def test_generate_story_success():
    """Should return a story when valid input is provided."""
    with patch("app.api.routes.stories.generate_story") as mock_generate:
        mock_generate.return_value = "This is a beautiful story about Tokyo."
        response = client.post("/api/stories/generate", json={
            "destination": "Tokyo",
            "travel_style": "foodie",
            "duration_days": 3,
            "preferences": "I love ramen",
            "language": "English"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["destination"] == "Tokyo"
        assert data["travel_style"] == "foodie"
        assert data["duration_days"] == 3
        assert "content" in data
        assert len(data["content"]) > 0


def test_generate_story_default_language():
    """Should default to English when language not specified."""
    with patch("app.api.routes.stories.generate_story") as mock_generate:
        mock_generate.return_value = "A story."
        response = client.post("/api/stories/generate", json={
            "destination": "Paris",
            "travel_style": "romantic",
            "duration_days": 2
        })
        assert response.status_code == 200