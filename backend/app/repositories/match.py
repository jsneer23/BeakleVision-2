from sqlmodel import or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Match, MatchCreate, MatchSimple

from .base import BaseRepository


class MatchRepository(BaseRepository[Match, MatchCreate]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Match, MatchCreate)

    async def get_by_team_and_event(self, team_key: str, event_key: str) -> list[Match]:
        statement = select(Match).where(
            Match.event_key == event_key,
            or_(
                Match.red_1 == team_key,
                Match.red_2 == team_key,
                Match.red_3 == team_key,
                Match.blue_1 == team_key,
                Match.blue_2 == team_key,
                Match.blue_3 == team_key,
            )
        )
        matches = await self.session.exec(statement)
        return matches.all()

    #TODO: Implement MatchSimple
    async def get_by_team_and_event_simple(self, team_key: str, event_key: str) -> list[MatchSimple]:
        statement = select(Match).where(
            Match.event_key == event_key,
            or_(
                Match.red_1 == team_key,
                Match.red_2 == team_key,
                Match.red_3 == team_key,
                Match.blue_1 == team_key,
                Match.blue_2 == team_key,
                Match.blue_3 == team_key,
            )
        )
        matches = await self.session.exec(statement)
        return matches.all()

    async def get_by_team_and_year(self, team_key: str, year: int) -> list[Match]:
        statement = select(Match).where(
            Match.year == year,
            or_(
                Match.red_1 == team_key,
                Match.red_2 == team_key,
                Match.red_3 == team_key,
                Match.blue_1 == team_key,
                Match.blue_2 == team_key,
                Match.blue_3 == team_key,
            )
        )
        matches = await self.session.exec(statement)
        return matches.all()

    #TODO: Implement MatchSimple
    async def get_by_team_and_year_simple(self, team_key: str, year: int) -> list[MatchSimple]:
        statement = select(Match).where(
            Match.year == year,
            or_(
                Match.red_1 == team_key,
                Match.red_2 == team_key,
                Match.red_3 == team_key,
                Match.blue_1 == team_key,
                Match.blue_2 == team_key,
                Match.blue_3 == team_key,
            )
        )
        matches = await self.session.exec(statement)
        return matches.all()
