from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models import Team
from app.services import TeamService

router = APIRouter(prefix="/team", tags=["team"])

@router.get(
    "/{number}",
    status_code=200,
)
async def get_team_by_number(number: int, session: SessionDep) -> Team:
    service = TeamService(session)
    return await service.get_by_number(number)
