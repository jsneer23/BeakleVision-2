from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.valkey import ValkeyCache
from app.models import Event, EventCreate, MatchCreate, TeamCreate, TeamEventCreate
from app.repositories import (
    EventRepository,
    MatchRepository,
    TeamEventRepository,
    TeamRepository,
)
from app.tba.utils import tba_api_call, validate_year


class TBAImportService:

    def __init__(self, session: AsyncSession, cache: ValkeyCache):
        self.event = EventRepository(session)
        self.match = MatchRepository(session)
        self.team = TeamRepository(session)
        self.team_event = TeamEventRepository(session)
        self.cache = cache

    async def _get_events(self, year: int) -> list[Event]:

        if not await self.event.year_exists(year):
            raise ValueError("Events for this year have not been loaded.")

        return await self.event.get_by_year(year)

    async def _import_team_events(self, event_key: str, year: int) -> None:

        endpoint: str = "event/" + event_key + "/teams/keys"
        team_keys = await tba_api_call(self.cache, endpoint)

        for team_key in team_keys:
            team_event = TeamEventCreate(
                team_key=team_key,
                event_key=event_key,
                year=year
            )
            await self.team_event.upsert(team_event)

    async def import_events(self, year: int) -> None:

        try:
            validate_year(year)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid year.")

        endpoint: str = "events/" + str(year)
        event_json = await tba_api_call(self.cache, endpoint)

        for event_dict in event_json:
            # Filter out preseason events
            if event_dict['event_type'] < 100:
                event_model = EventCreate(**event_dict)
                await self.event.upsert(event_model)
                await self._import_team_events(event_dict['key'], year)

    async def import_teams(self) -> None:

        for i in range(30):
            endpoint: str = "teams/" + str(i)
            team_json = await tba_api_call(self.cache, endpoint)


            for team_dict in team_json:
                team_model = TeamCreate(**team_dict)
                await self.team.upsert(team_model)

    async def import_matches(self, year: int) -> int:

        try:
            validate_year(year)

            events = await self._get_events(year)
            event_keys = [event.key for event in events]
        except ValueError:
            raise HTTPException(status_code=400,
                                detail=f"Error fetching events. Try running /tba/events/{year}"
                                " first or enter a valid year.")

        matches = 0

        for event_key in event_keys:

            endpoint: str = "event/" + event_key + "/matches"
            match_json = await tba_api_call(self.cache, endpoint)

            for match_dict in match_json:
                matches += 1
                match_model = MatchCreate(**match_dict)
                await self.match.upsert(match_model)

        return matches
