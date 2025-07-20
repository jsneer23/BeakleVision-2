from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Event, EventCreate
from app.repositories import EventRepository
from app.tba.utils import valid_event, validate_year


class EventService:

    def __init__(self, session: AsyncSession):
        self.repo = EventRepository(session)

    async def from_tba(self, event_dict: dict[str, Any]) -> Event | None:

        if not valid_event(event_dict):
            return None

        event = EventCreate(**event_dict)
        return await self.repo.upsert(event)

    async def events_loaded_throws_error(self, year: int) -> None:
        validate_year(year)

        if not await self.repo.year_exists(year):
            raise ValueError("Events for this year have not been loaded.")

    async def get_events(self, year: int) -> list[Event]:
        await self.events_loaded_throws_error(year)

        return await self.repo.get_events_by_year(year)
