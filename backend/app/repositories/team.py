from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Team, TeamCreate

from .base import BaseRepository


class TeamRepository(BaseRepository[Team, TeamCreate]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Team, TeamCreate)

