from typing import TYPE_CHECKING, Annotated

from pydantic import AfterValidator
from sqlmodel import Field, Relationship, SQLModel

from app.tba.utils import validate_year

if TYPE_CHECKING:
    from .event import Event


class YearStatsBase(SQLModel):
    year: int

    #TODO implement year statistics


class YearStatsCreate(YearStatsBase):
    year: Annotated[int, AfterValidator(validate_year)]


class YearStats(YearStatsBase, table=True):
    """
    SQL table that holds year specific statistics.
    """
    year: int = Field(primary_key=True)

    events: list["Event"] = Relationship(back_populates="year_stats")#2
