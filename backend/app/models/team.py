import uuid
from typing import Annotated, Any

from pydantic import AfterValidator, field_validator, model_validator
from sqlmodel import Field, Relationship, SQLModel

from app.tba.constants import District, StateProv
from app.tba.utils import validate_year

from .utils import get_state_prov, strip_string


class TeamBase(SQLModel):
    """
    Base Pydantic/SQLmodel that holds team specific information from TBA
    """
    key: Annotated[str, AfterValidator(strip_string)]
    number: int
    name: Annotated[str, AfterValidator(strip_string)]
    rookie_year: Annotated[int | None, AfterValidator(validate_year)]
    country: Annotated[str | None, AfterValidator(strip_string)]
    state_prov: StateProv
    city: Annotated[str | None, AfterValidator(strip_string)]


class TeamCreate(TeamBase):
    """
    SQL table that holds team specific information from TBA
    """

    @model_validator(mode="before")
    @classmethod
    def validate_team(cls, team_dict: dict[str, Any]) -> dict[str, Any]:
        team_dict["number"] = team_dict["key"].strip()[3:]
        return team_dict

    @field_validator("state_prov", mode="before")
    @classmethod
    def validate_state_prov(cls, v: str | None) -> StateProv:
        fixed = get_state_prov(v)
        return StateProv(fixed)


class Team(TeamBase, table=True):

    key: Annotated[str, AfterValidator(strip_string)] = Field(primary_key=True)

    district: District = Field(default=District("")) #TODO Implement district

    year_stats: list["TeamYearStats"] = Relationship(back_populates="team") #1


class TeamYearStats(SQLModel, table=True):
    """
    SQL table that holds team specific statistics for a given year.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    key: str = Field(foreign_key="team.key")
    year: int = Field(foreign_key="yearstats.year")

    team: "Team" = Relationship(back_populates="year_stats") #1

    # TODO: Add fields for year stats as needed
