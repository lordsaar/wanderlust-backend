import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Story(Base):
    __tablename__ = "stories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    destination = Column(String(100), nullable=False)
    travel_style = Column(String(50), nullable=False)
    duration_days = Column(Integer, nullable=False)
    language = Column(String(20), nullable=False, default="English")
    preferences = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
