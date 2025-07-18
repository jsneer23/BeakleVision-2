from app.models.match import Match, MatchCreate

from .base import BaseRepository


class MatchRepository(BaseRepository):

    def upsert(self, update_match: MatchCreate) -> Match:

        match = Match.model_validate(update_match)
        db_model = self.session.merge(match)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model
