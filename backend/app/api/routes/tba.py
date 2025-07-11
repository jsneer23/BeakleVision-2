import multiprocessing

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import (  # noqa: F401
    SessionDep,
    ValkeyDep,
    get_current_active_superuser,
)
from app.crud.tba_init import (
    create_or_update_event,
    create_or_update_match,
    create_or_update_team,
)
from app.models.app import Message
from app.models.base import Event, Match, Team
from app.models.helpers import valid_event, valid_match
from app.tba.main import tba_api_call

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
            team_model: Team = Team(team)
            create_or_update_team(session, team_model)

    return Message(message="Fetched teams.")


@router.put(
    "/events/{year}",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def init_events(session: SessionDep, cache: ValkeyDep, year: int) -> Message:
    """
    Get teams.
    """

    if year < 1992 or year > 2026:
        raise HTTPException(status_code=400, detail="Invalid year.")

    endpoint: str = "events/" + str(year)
    event_json = await tba_api_call(cache, endpoint)

    for event in event_json:

        if not valid_event(event):
            continue

        event_model= Event(event)

        create_or_update_event(session, event_model)

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

    if year < 1992 or year > 2026:
        raise HTTPException(status_code=400, detail="Invalid year.")

    statement = select(Event).where(Event.year == year)
    events = session.exec(statement)

    if not events.first():
        raise HTTPException(status_code=404, detail="No events found for this year. Try fetching events first.")

    events = session.exec(statement)
    for event in events:

        endpoint: str = "event/" + event.key + "/matches"
        match_json = await tba_api_call(cache, endpoint)

        print(f"Processing matches for event: {event.key}")

        for match in match_json:

            if not valid_match(match):
                continue

            #print("Processing match:", match["key"])
            match_model = Match(match, year)

            create_or_update_match(session, match_model)

    return Message(message="Fetched matches.")
