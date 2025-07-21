from sqlmodel import SQLModel


class EventSearch(SQLModel):

    name: str
    key: str

class TeamSearch(SQLModel):

    number: int
    nickname: str


class SearchIndex(SQLModel):
    events: list["EventSearch"] = []
    teams: list["TeamSearch"] = []
