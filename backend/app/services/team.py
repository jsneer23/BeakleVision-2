from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Team, TeamCreate
from app.repositories import TeamRepository


class TeamService:

    def __init__(self, session: AsyncSession):
        self.repo = TeamRepository(session)

    async def from_tba(self, team_dict: dict[str, Any]):

        team = TeamCreate(**team_dict)

        await self.repo.upsert(team)
