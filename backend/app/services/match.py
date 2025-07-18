from typing import Any

from sqlmodel import Session

from app.models.match import MatchCreate
from app.repositories.match import MatchRepository


class MatchService:
    def __init__(self, session: Session):
        self.repo = MatchRepository(session)

    def from_tba(self, match_dict: dict[str, Any]) -> None:

        match = MatchCreate(**match_dict)

        self.repo.upsert(match)
