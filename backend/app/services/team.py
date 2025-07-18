from typing import Any

from sqlmodel import Session

from app.models.team import TeamCreate
from app.repositories.team import TeamRepository


class TeamService:

    def __init__(self, session: Session):
        self.repo = TeamRepository(session)

    def from_tba(self, team_dict: dict[str, Any]):

        team = TeamCreate(**team_dict)

        self.repo.upsert(team)

