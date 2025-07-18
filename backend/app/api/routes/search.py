from fastapi import APIRouter

from app.models.match import Event, Team

@router.get(
    "/teams/",
    #dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
async def search_index(session: SessionDep) -> Message:
    pass