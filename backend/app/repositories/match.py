from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Match, MatchCreate

from .base import BaseRepository


class MatchRepository(BaseRepository[Match, MatchCreate]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Match, MatchCreate)
