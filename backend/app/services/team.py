from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Event, Match, Team
from app.repositories import (
    EventRepository,
    MatchRepository,
    TeamEventRepository,
    TeamRepository,
)


class TeamService:
    """
    Service layer that provides data to the team page located at /team/{$teamNumber}/{-$year}
    """

    def __init__(self, session: AsyncSession):
        self.event = EventRepository(session)
        self.match = MatchRepository(session)
        self.team_event = TeamEventRepository(session)
        self.team = TeamRepository(session)

    async def get_by_key(self, team_key: str) -> Team:
        team = await self.team.get_by_key(team_key)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team

    async def get_events_by_year(self, team_key: str, year: int) -> list[Event]:
        team_events = await self.team_event.get_by_team_and_year(team_key, year)
        team_events.sort(key=lambda x: x.start_date)
        return team_events

    async def get_matches_by_event(self, team_key: str, event_key: str) -> list[Match]:
        return await self.match.get_by_team_and_event(team_key, event_key)

    async def get_matches_by_year(self, team_key: str, year: int) -> list[Match]:
        return await self.match.get_by_team_and_year(team_key, year)
