from app.models.team import Team, TeamCreate

from .base import BaseRepository


class TeamRepository(BaseRepository):

    def upsert(self, update_team: TeamCreate) -> Team:

        team = Team.model_validate(update_team)
        db_model = self.session.merge(team)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model

