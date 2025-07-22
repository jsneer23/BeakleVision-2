from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Event
from app.repositories import EventRepository


class EventService:

    def __init__(self, session: AsyncSession):
        self.event = EventRepository(session)

    async def get_by_key(self, key: str) -> Event:
        event = await self.event.get_by_key(key)
        if not isinstance(event, Event):
            raise HTTPException(status_code=404, detail="Event not found")
        return event
