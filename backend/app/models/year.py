from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .event import Event

class YearStats(SQLModel, table=True):
    """
    SQL table that holds year specific statistics.
    """
    year: int = Field(primary_key=True)

    events: list["Event"] = Relationship(back_populates="year_stats")#2

    @field_validator('year')
    @classmethod
    def validate_year(cls, v: int) -> int:
        if not (1992 <= v <= 2026):
            raise ValueError("Year must be between 1992 and 2026.")
        return v
