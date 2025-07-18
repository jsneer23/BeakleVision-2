from fastapi import APIRouter, HTTPException

from app.api.deps import (  # noqa: F401
    SessionDep,
    ValkeyDep,
    get_current_active_superuser,
)
from app.models.app import Message
from app.services.event import EventService
from app.services.match import MatchService
from app.services.team import TeamService
from app.tba.main import tba_api_call
from app.tba.utils import validate_year

router = APIRouter(prefix="/tba", tags=["tba"])


@router.put(
    "/teams/",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def init_teams(session: SessionDep, cache: ValkeyDep) -> Message:
    """
    Get teams.
    """

    for i in range(30):
        endpoint: str = "teams/" + str(i)
        team_json = await tba_api_call(cache, endpoint)

        team_service = TeamService(session)

        for team in team_json:
            team_service.from_tba(team)

    return Message(message="Fetched teams.")


@router.put(
    "/events/{year}",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def init_events(session: SessionDep, cache: ValkeyDep, year: int) -> Message:
    """
    Get Events
    """

    try:
        validate_year(year)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid year.")

    endpoint: str = "events/" + str(year)
    event_json = await tba_api_call(cache, endpoint)

    event_service = EventService(session)

    for event in event_json:
        event_service.from_tba(event)

    return Message(message="Fetched events.")

@router.put(
    "/matches/{year}",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def init_matches(session: SessionDep, cache: ValkeyDep, year: int) -> Message:
    """
    Get matches.
    """

    event_service = EventService(session)

    try:
        events = event_service.get_events(year)
    except ValueError:
        raise HTTPException(status_code=400, detail="Error fetching events. Try running /tba/events/{year} first or enter a valid year.")

    match_service = MatchService(session)

    matches = 0

    for event in events:

        endpoint: str = "event/" + event.key + "/matches"
        match_json = await tba_api_call(cache, endpoint)

        for match in match_json:
            matches += 1
            match_service.from_tba(match)

    return Message(message=f"Fetched {matches} matches.")
