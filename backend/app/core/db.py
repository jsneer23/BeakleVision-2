from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.crud import app as app_crud
from app.models import (  # noqa: F401
    Event,
    Match,
    Team,
    TeamEvent,
    TeamYearStats,
    YearStats,
)
from app.models.app import User, UserCreate
from app.services.year import YearStatsService

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


async def init_db(session: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    #from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    #SQLModel.metadata.create_all(engine)

    user = await session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER))
    if not user.first():
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = await app_crud.create_user(session=session, user_create=user_in)

    await YearStatsService(session).init_year_db()
