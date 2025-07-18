from sqlmodel import Session, SQLModel


class BaseRepository:

    def __init__(self, session: Session):
        self.session: Session = session

    def delete(self, model: SQLModel) -> None:
        self.session.delete(model)
        self.session.commit()

    def get_by_key(self, key: str) -> SQLModel | None:
        return self.session.get(model_type=SQLModel, key=key)
