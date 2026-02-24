import anthropic
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

async def generate_story(
    destination: str,
    travel_style: str,
    duration_days: int,
    preferences: str = ""
) -> str:
    prompt = f"""You are a gifted travel writer. Write a vivid, narrative day-by-day travel story for the following trip:

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
    return message.content[0].text
