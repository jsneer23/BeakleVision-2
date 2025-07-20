from fastapi import APIRouter, HTTPException

from app.api.deps import (  # noqa: F401
    SessionDep,
    ValkeyDep,
    get_current_active_superuser,  # TODO require login to call these endpoints???
)
from app.core.db import AsyncSessionLocal
from app.models.app import Message
from app.services import EventService, MatchService, TeamService
from app.tba.utils import tba_api_call, validate_year

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


        for team in team_json:
            await TeamService(session).from_tba(team)

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

    for event in event_json:
        await EventService(session).from_tba(event)

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

    try:
        events = await EventService(session).get_events(year)
        event_keys = [event.key for event in events]
    except ValueError:
        raise HTTPException(status_code=400,
                            detail=f"Error fetching events. Try running /tba/events/{year}"
                            " first or enter a valid year.")

    matches = 0

    for event_key in event_keys:

        endpoint: str = "event/" + event_key + "/matches"
        match_json = await tba_api_call(cache, endpoint)

        print(f"Processing event {event_key}")

        for match in match_json:
            matches += 1
            await MatchService(session).from_tba(match)

    return Message(message=f"Fetched {matches} matches.")
