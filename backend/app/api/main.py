from fastapi import APIRouter

from app.api.routes import event, items, login, private, tba, team, users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(tba.router)
api_router.include_router(event.router)
api_router.include_router(team.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
