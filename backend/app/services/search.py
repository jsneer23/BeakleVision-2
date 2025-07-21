from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models import SearchIndex
from app.repositories import EventRepository, TeamRepository


class SearchService:

    def __init__(self, session: AsyncSession):
        self.event = EventRepository(session)
        self.team = TeamRepository(session)

    async def search_index(self) -> SearchIndex:
        events = await self.event.search_index()
        teams = await self.team.search_index()

        return SearchIndex(events=events, teams=teams)
