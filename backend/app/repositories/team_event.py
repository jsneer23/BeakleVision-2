from sqlmodel import select

from app.models.team_event import TeamEvent, TeamEventCreate

from .base import BaseRepository


class TeamEventRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, TeamEvent, TeamEventCreate)

    async def get_by_team_and_year(self, team_key: str, year: int) -> list[TeamEvent]:
        statement = select(TeamEvent).where(
            TeamEvent.team_key == team_key,
            TeamEvent.year == year
        )
        team_events = await self.session.exec(statement)
        return team_events.all()
