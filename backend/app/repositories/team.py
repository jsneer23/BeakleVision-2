from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Team, TeamCreate
from app.models.search import TeamSearch

from .base import BaseRepository


class TeamRepository(BaseRepository[Team, TeamCreate]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Team, TeamCreate)

    async def search_index(self) -> list[TeamSearch]:
        """
        Get all teams.
        """
        statement = select(Team.nickname, Team.number)
        teams = await self.session.exec(statement)
        return teams.all()
