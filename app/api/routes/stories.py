from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.claude_service import generate_story

router = APIRouter()

class StoryRequest(BaseModel):
    destination: str
    travel_style: str
    duration_days: int
    preferences: str = ""
    language: str = "English"

class StoryResponse(BaseModel):
    destination: str
    travel_style: str
    duration_days: int
    content: str

@router.post("/generate", response_model=StoryResponse)
async def create_story(request: StoryRequest):
    if not request.destination:
        raise HTTPException(status_code=400, detail="Destination is required")
    content = await generate_story(
        destination=request.destination,
        travel_style=request.travel_style,
        duration_days=request.duration_days,
        preferences=request.preferences,
        language=request.language
    )
    return StoryResponse(
        destination=request.destination,
        travel_style=request.travel_style,
        duration_days=request.duration_days,
        content=content
    )
