import anthropic
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

async def generate_story(
    destination: str,
    travel_style: str,
    duration_days: int,
    preferences: str = "",
    language: str = "English"
) -> str:
    prompt = f"""You are a gifted travel writer. You must write ENTIRELY in {language}. Every single word of the story must be in {language}. Do not use any other language. Write a vivid, narrative day-by-day travel story for the following trip:

Destination: {destination}
Travel style: {travel_style}
Duration: {duration_days} days
Personal preferences: {preferences if preferences else "none specified"}

Write in rich, evocative prose — not bullet points. Make the reader feel like they are there.
Each day should flow naturally into the next. Begin with arrival and end with departure.
Aim for approximately 150 words per day."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    
    block = message.content[0]
    if hasattr(block, 'text'):
        return block.text
    raise ValueError("Unexpected response type from Claude API")