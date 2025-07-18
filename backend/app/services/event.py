from typing import Any

from sqlmodel import Session

from app.models.event import Event, EventCreate
from app.repositories.event import EventRepository
from app.tba.utils import valid_event, validate_year


def _process_event_json(event_dict: dict[str, Any]) -> None:
    if isinstance(event_dict['district'], dict):
        event_dict['district'] = event_dict.get('district', {}).get('abbreviation', None)


class EventService:

    def __init__(self, session: Session):
        self.repo = EventRepository(session)

    def from_tba(self, event_dict: dict[str, Any]) -> Event | None:

        if not valid_event(event_dict):
            return None

        _process_event_json(event_dict)

        event = EventCreate(**event_dict)
        return self.repo.upsert(event)

    def events_loaded(self, year: int) -> None:
        validate_year(year)

        if not self.repo.year_exists(year):
            raise ValueError("Events for this year have not been loaded.")

    def get_events(self, year: int) -> list[Event]:
        self.events_loaded(year)
        return self.repo.get_events_by_year(year)
