from fastapi import APIRouter

from app.api.deps import (  # noqa: F401
    SessionDep,
    ValkeyDep,
    get_current_active_superuser,  # TODO require login to call these endpoints???
)
from app.models.app import Message
from app.services import TBAImportService

router = APIRouter(prefix="/tba", tags=["tba"])


@router.put(
    "/teams/",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def init_teams(session: SessionDep, cache: ValkeyDep) -> Message:
    """
    Get teams from The Blue Alliance (TBA) API for data initialization.
    """

    await TBAImportService(session, cache).import_teams()

    return Message(message="Fetched teams.")


@router.put(
    "/events/{year}",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def init_events(session: SessionDep, cache: ValkeyDep, year: int) -> Message:
    """
    Get Events for {year} from The Blue Alliance (TBA) API for data initialization.
    """

    await TBAImportService(session, cache).import_events(year)

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

    matches = await TBAImportService(session, cache).import_matches(year)

    return Message(message=f"Fetched {matches} matches.")
