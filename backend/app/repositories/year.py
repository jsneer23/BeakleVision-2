from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models import YearStats, YearStatsCreate

from .base import BaseRepository


class YearStatsRepository(BaseRepository[YearStats, YearStatsCreate]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, YearStats, YearStatsCreate)
