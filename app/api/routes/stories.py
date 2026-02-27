import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.models.story import Story
from app.core.database import get_db
from app.services.claude_service import generate_story
from pydantic import BaseModel, Field

router = APIRouter()

class StoryRequest(BaseModel):
    destination: str = Field(min_length=1, max_length=100)
    travel_style: str = Field(min_length=1, max_length=50)
    duration_days: int = Field(ge=1, le=30)
    language: str = Field(default="English", max_length=20)
    preferences: str = Field(default="", max_length=500)

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
def get_stories(db: Session = Depends(get_db), limit: int = Query(default=10, ge=1, le=100)):
    stories = db.query(Story).order_by(Story.created_at.desc()).limit(limit).all()
    return stories

@router.delete("/{story_id}")
def delete_story(story_id: str, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    db.delete(story)
    db.commit()
    return {"message": "Story deleted"}