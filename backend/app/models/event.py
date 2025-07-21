from datetime import date
from typing import TYPE_CHECKING, Annotated, Any

from pydantic import AfterValidator, ValidationInfo, field_validator, model_validator
from sqlmodel import Field, Relationship, SQLModel

from app.tba.constants import District, EventType, StateProv
from app.tba.utils import validate_year

from .utils import get_district, get_state_prov, strip_string

if TYPE_CHECKING:
    from .match import Match
    from .year import YearStats

class EventBase(SQLModel):
    """
    Base Pydantic/SQLModel that holds event specific information from TBA.
    """
    year: Annotated[int, AfterValidator(validate_year)]
    key: Annotated[str, AfterValidator(strip_string)]

    name: Annotated[str, AfterValidator(strip_string)]
    country: Annotated[str | None, AfterValidator(strip_string)]
    state_prov: StateProv
    city: Annotated[str | None, AfterValidator(strip_string)]
    district: District
    start_date: date
    end_date: date
    event_type: EventType
    week: int


class EventCreate(EventBase):

    @model_validator(mode="before")
    @classmethod
    def validate_event(cls, event_dict: dict[str, Any]) -> dict[str, Any]:

        if isinstance(event_dict['district'], dict):
            event_dict['district'] = event_dict.get('district', {}).get('abbreviation', None)

        if not isinstance(event_dict['week'], int):
            event_dict['week'] = -1

        return event_dict

    @field_validator("state_prov", mode="before")
    @classmethod
    def validate_state_prov(cls, v: str | None) -> StateProv | None:
        return get_state_prov(v)

    @field_validator("district", mode="before")
    @classmethod
    def validate_district(cls, v: str | None) -> District:
        return get_district(v)

    @field_validator("week")
    @classmethod
    def validate_week(cls, v: int | None, info: ValidationInfo) -> int:

        if EventType(info.data['event_type']).is_champs:
            return 8
        if EventType(info.data['event_type']).is_offseason:
            return 9
        if v is -1:
            raise ValueError("Event week is None for a non championship event, this should not happen.")

        return v+1


class Event(EventBase, table=True):
    """
    SQL table that holds event specific information from TBA.
    """
    year: Annotated[int, AfterValidator(validate_year)] = Field(foreign_key="yearstats.year")
    key: Annotated[str, AfterValidator(strip_string)] = Field(primary_key=True)

    year_stats: "YearStats" = Relationship(back_populates="events") #2
    matches: list["Match"] = Relationship(back_populates="event_info") #3
