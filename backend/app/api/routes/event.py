from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models import Event
from app.services import EventService

router = APIRouter(prefix="/event", tags=["event"])

@router.get(
    "/{key}",
    status_code=200,
)
async def event(key: str, session: SessionDep) -> Event:
    service = EventService(session)
    return await service.get_by_key(key)
