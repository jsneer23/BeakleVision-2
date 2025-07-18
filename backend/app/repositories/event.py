from sqlmodel import select

from app.models.event import Event, EventCreate

from .base import BaseRepository


class EventRepository(BaseRepository):

    def upsert(self, update_event: EventCreate) -> Event:
        event = Event.model_validate(update_event)
        db_model = self.session.merge(event)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model

    def year_exists(self, year: int) -> bool:
        """
        Check if any events for the given year exist in the database.
        """
        statement = select(Event).where(Event.year == year)
        events = self.session.exec(statement)
        return events.first() is not None

    def get_events_by_year(self, year: int) -> list[Event]:
        """
        Get all events for a given year.
        """
        statement = select(Event).where(Event.year == year)
        events = self.session.exec(statement).all()
        return events
