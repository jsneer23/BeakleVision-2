from sqlmodel import Session, select

from app.models.event import Event
from app.models.match import Match
from app.models.team import Team
from app.models.year import YearStats


def create_team(*, session: Session, team_in: Team) -> Team:
    session.add(team_in)
    session.commit()
    session.refresh(team_in)
    return team_in

def update_team(*, session: Session, db_team: Team, update_team: Team) -> Team:
    db_team.sqlmodel_update(update_team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

def create_or_update_team(session: Session, team_in: Team) -> Team:

    statement = select(Team).where(Team.key == team_in.key)
    existing_team = session.exec(statement).first()

    if existing_team:
        return update_team(session=session, db_team=existing_team, update_team=team_in)
    else:
        return create_team(session=session, team_in=team_in)


def create_event(*, session: Session, event_in: Event) -> Event:
    session.add(event_in)
    session.commit()
    session.refresh(event_in)
    return event_in

def update_event(*, session: Session, db_event: Event, update_event: Event) -> Event:
    db_event.sqlmodel_update(update_event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

def create_or_update_event(
    session: Session, event_in: Event
) -> Event:

    statement = select(Event).where(Event.key == event_in.key)
    existing_event = session.exec(statement).first()

    if existing_event:
        return update_event(session=session, db_event=existing_event, update_event=event_in)
    else:
        return create_event(session=session, event_in=event_in)


def create_year_stats(*, session: Session, year_stats_in: YearStats) -> YearStats:
    db_year_stats = YearStats.model_validate(year_stats_in)
    session.add(db_year_stats)
    session.commit()
    session.refresh(db_year_stats)
    return db_year_stats

def update_year_stats(*, session: Session, db_year_stats: YearStats, update_year_stats: YearStats) -> YearStats:
    db_year_stats.sqlmodel_update(update_year_stats)
    session.add(db_year_stats)
    session.commit()
    session.refresh(db_year_stats)
    return db_year_stats

def create_or_update_year_stats(
    session: Session, year_stats_in: YearStats
) -> YearStats:

    statement = select(YearStats).where(YearStats.year == year_stats_in.year)
    existing_year_stats = session.exec(statement).first()

    if existing_year_stats:
        return update_year_stats(session=session, db_year_stats=existing_year_stats, update_year_stats=year_stats_in)
    else:
        return create_year_stats(session=session, year_stats_in=year_stats_in)

def create_match(*, session: Session, match_in: Match) -> Match:
    session.add(match_in)
    session.commit()
    session.refresh(match_in)
    return match_in

def update_match(*, session: Session, db_match: Match, update_match: Match) -> Match:
    db_match.sqlmodel_update(update_match)
    session.add(db_match)
    session.commit()
    session.refresh(db_match)
    return db_match

def create_or_update_match(
    session: Session, match_in: Match
) -> Match:

    statement = select(Match).where(Match.key == match_in.key)
    existing_match = session.exec(statement).first()

    if existing_match:
        return update_match(session=session, db_match=existing_match, update_match=match_in)
    else:
        return create_match(session=session, match_in=match_in)
