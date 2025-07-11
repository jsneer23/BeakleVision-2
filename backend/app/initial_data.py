import logging

from sqlmodel import Session

from app.core.db import engine, init_db
from app.crud.tba_init import create_or_update_year_stats
from app.models.base import YearStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_years(session: Session) -> None:
    for year in range(1992, 2027):
        year_stats = YearStats(year=year)
        create_or_update_year_stats(session=session, year_stats_in=year_stats)


def init() -> None:
    with Session(engine) as session:
        init_db(session)
        init_years(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
