from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Match, MatchCreate
from app.repositories import MatchRepository


class MatchService:
    def __init__(self, session: AsyncSession):
        self.repo = MatchRepository(session)

    async def from_tba(self, match_dict: dict[str, Any]) -> None:

        match = MatchCreate(**match_dict)

        await self.repo.upsert(match)
