from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import YearStats, YearStatsCreate
from app.repositories import YearStatsRepository


class YearStatsService:

    def __init__(self, session: AsyncSession):
        self.repo = YearStatsRepository(session)

    async def init_year_db(self):
        for year in range(1992, 2027):
            #TODO get rid of upsert by checking if year exists
            await self.repo.upsert(YearStatsCreate(year=year))
