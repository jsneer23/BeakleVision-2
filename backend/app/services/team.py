from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Team
from app.repositories import TeamRepository


class TeamService:

    def __init__(self, session: AsyncSession):
        self.team = TeamRepository(session)

    async def get_by_key(self, key: str) -> Team:
        team = await self.team.get_by_key(key)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team

    async def get_by_number(self, number: int) -> Team:
        return await self.get_by_key("frc" + str(number))
