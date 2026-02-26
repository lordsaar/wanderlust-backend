import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.story import Story
from app.core.database import get_db
from app.services.claude_service import generate_story
from pydantic import BaseModel

router = APIRouter()

class StoryRequest(BaseModel):
    destination: str
    travel_style: str
    duration_days: int
    language: str = "English"
    preferences: str = ""

class StoryResponse(BaseModel):
    id: str
    destination: str
    travel_style: str
    duration_days: int
    language: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/generate", response_model=StoryResponse)
async def generate_story_endpoint(request: StoryRequest, db: Session = Depends(get_db)):
    if not request.destination.strip():
        raise HTTPException(status_code=400, detail="Destination cannot be empty")

    content = await generate_story(
        destination=request.destination,
        travel_style=request.travel_style,
        duration_days=request.duration_days,
        language=request.language,
        preferences=request.preferences
    )

    story = Story(
        id=str(uuid.uuid4()),
        destination=request.destination,
        travel_style=request.travel_style,
        duration_days=request.duration_days,
        language=request.language,
        preferences=request.preferences,
        content=content,
        created_at=datetime.utcnow()
    )
    db.add(story)
    db.commit()
    db.refresh(story)

    return story

@router.get("/", response_model=list[StoryResponse])
def get_stories(db: Session = Depends(get_db), limit: int = 10):
    stories = db.query(Story).order_by(Story.created_at.desc()).limit(limit).all()
    return stories
