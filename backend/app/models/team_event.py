import uuid
from typing import TYPE_CHECKING, Annotated

from pydantic import AfterValidator
from sqlmodel import Field, Relationship, SQLModel

from .utils import strip_string

if TYPE_CHECKING:
    from .event import Event
    from .team import Team

class TeamEventBase(SQLModel):

    team_key: Annotated[str, AfterValidator(strip_string)]
    event_key: Annotated[str, AfterValidator(strip_string)]
    year: int

class TeamEventCreate(TeamEventBase):
    pass

class TeamEvent(TeamEventBase, table=True):
    """
    SQL table that holds event specific information from TBA.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    team_key: str = Field(foreign_key="team.key")
    event_key: str = Field(foreign_key="event.key")

    event: "Event" = Relationship(back_populates="teams") #4
    team: "Team" = Relationship(back_populates="events") #5
