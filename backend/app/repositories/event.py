from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Event, EventCreate

from .base import BaseRepository


class EventRepository(BaseRepository[Event, EventCreate]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Event, EventCreate)

    async def year_exists(self, year: int) -> bool:
        """
        Check if any events for the given year exist in the database.
        """
        statement = select(Event.key).where(Event.year == year)
        events = await self.session.exec(statement)
        return events.first() is not None

    async def get_events_by_year(self, year: int) -> list[Event]:
        """
        Get all events for a given year.
        """
        statement = select(Event).where(Event.year == year)
        events = await self.session.exec(statement)
        return events.all()
