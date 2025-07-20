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
async def init_teams(cache: ValkeyDep) -> Message:
    """
    Get teams.
    """

    for i in range(30):
        endpoint: str = "teams/" + str(i)
        team_json = await tba_api_call(cache, endpoint)


        for team in team_json:
            async with AsyncSessionLocal() as session:
                await TeamService(session).from_tba(team)

    return Message(message="Fetched teams.")


@router.put(
    "/events/{year}",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def init_events(cache: ValkeyDep, year: int) -> Message:
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
        async with AsyncSessionLocal() as session:
            await EventService(session).from_tba(event)

    return Message(message="Fetched events.")


@router.put(
    "/matches/{year}",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def init_matches(cache: ValkeyDep, year: int) -> Message:
    """
    Get matches.
    """

    async with AsyncSessionLocal() as session:
        try:
            events = await EventService(session).get_events(year)
        except ValueError:
            raise HTTPException(status_code=400,
                                detail=f"Error fetching events."
                                f"Try running /tba/events/{year}"
                                " first or enter a valid year.")

    matches = 0

    for event in events:

        endpoint: str = "event/" + event.key + "/matches"
        match_json = await tba_api_call(cache, endpoint)

        print(f"Processing event {event.key}")

        for match in match_json:
            matches += 1
            async with AsyncSessionLocal() as session:
                await MatchService(session).from_tba(match)

    return Message(message=f"Fetched {matches} matches.")
