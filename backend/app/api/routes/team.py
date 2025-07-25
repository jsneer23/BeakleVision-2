from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models import Event, Match, Team, TeamEvent
from app.services import TeamService

router = APIRouter(prefix="/team", tags=["team"])

@router.get(
    "/{key}",
    status_code=200,
)
async def get_team_by_key(key: str, session: SessionDep) -> Team:
    service = TeamService(session)
    return await service.get_by_key(key)

@router.get(
    "/{key}/events/{year}",
    response_model=list[Event],
    status_code=200,
)
async def get_events_by_year(key: str, year: int, session: SessionDep) -> list[Event]:
    service = TeamService(session)
    return await service.get_events_by_year(key, year)

@router.get(
    "/{team_key}/event/{event_key}/matches",
    response_model=list[Match],
    status_code=200,
)
async def get_matches_by_event(team_key: str, event_key: str, session: SessionDep) -> list[Match]:
    service = TeamService(session)
    return await service.get_matches_by_event(team_key, event_key)

@router.get(
    "/{team_key}/matches/{year}",
    response_model=list[Match],
    status_code=200,
)
async def get_matches_by_year(team_key: str, year: int, session: SessionDep) -> list[Match]:
    service = TeamService(session)
    return await service.get_matches_by_year(team_key, year)
