import uuid
from typing import Any, cast

from sqlmodel import Field, Relationship, SQLModel

from app.models.helpers import (
    get_date_from_str,
    get_district,
    get_state_prov,
    get_time_from_int,
    get_video,
)
from app.models.utils import EventType, MatchStatus, MatchType, MatchWinner
from app.tba.constants import BREAKDOWN_MAPPINGS


class Team(SQLModel, table=True):
    """
    SQL table that holds team specific information from TBA
    """
    key: str = Field(primary_key=True)
    number: str
    name: str
    rookie_year: int | None
    country: str | None
    state: str | None
    city: str | None
    district: str | None

    year_stats: list["TeamYearStats"] = Relationship(back_populates="team") #1

    def __init__(self, team: dict[str, Any]) -> None:
        self.key= team["key"]
        self.number= team["key"][3:]
        self.name= team["nickname"]
        self.rookie_year= int(team["rookie_year"]) if team["rookie_year"] else None
        self.district= None  # Maybe remove?
        self.country= team["country"]
        self.state= team["state_prov"]
        self.city= team["city"]

class YearStats(SQLModel, table=True):
    """
    SQL table that holds year specific statistics.
    """
    year: int = Field(primary_key=True)

    events: list["Event"] = Relationship(back_populates="year_stats") #2

class TeamYearStats(SQLModel, table=True):
    """
    SQL table that holds team specific statistics for a given year.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    key: str = Field(foreign_key="team.key")
    year: int = Field(foreign_key="yearstats.year")

    team: Team = Relationship(back_populates="year_stats") #1

class Event(SQLModel, table=True):
    """
    SQL table that holds event specific information from TBA.
    """
    year: int = Field(foreign_key="yearstats.year")
    key: str = Field(primary_key=True)

    year_stats: YearStats = Relationship(back_populates="events") #2
    matches: list["Match"] = Relationship(back_populates="event_info") #3

    name: str
    country: str | None
    state: str | None
    city: str | None
    district: str | None
    start_date: str
    end_date: str
    time: int
    type: EventType
    week: int
    video: str | None

    def __init__(self, event: dict[str, Any]) -> None:
        if event["week"] is None and EventType(event["event_type"]).not_champs:
            raise ValueError("Event week is None, this should not happen.")

        self.year = int(event["year"])
        self.key = event["key"]
        self.name = event["name"]
        self.country = event["country"]
        self.state = get_state_prov(event["state_prov"])
        self.city = event["city"]
        self.district = get_district(event["district"]["abbreviation"]) if event["district"] else None
        self.start_date = event["start_date"]
        self.end_date = event["end_date"]
        self.time = get_date_from_str(event["start_date"])
        self.type = EventType(event["event_type"])
        self.week = int(event["week"])+1 if event["week"] is not None else -1
        self.video = get_video(event["webcasts"])

        if self.type.is_champs:
            self.week = 8

        if self.type.is_offseason:
            self.week = 9


class Match(SQLModel, table=True):
    """
    SQL table that holds match breakdown information that comes with each match
    download from TBA. Each match has a match breakdown.

    The breakdown is different for each season. For more info see the TBA API at
    https://www.thebluealliance.com/apidocs/v3 and look at src.tba.breakdown to
    see how the API values are converted into values here.
    """
    year: int = Field(foreign_key="yearstats.year")
    event: str = Field(foreign_key="event.key")
    key: str = Field(primary_key=True)

    event_info: Event = Relationship(back_populates="matches") #3

    match_type: MatchType
    set_number: int
    match_number: int
    status: MatchStatus
    video: str | None
    red_1: str
    red_2: str
    red_3: str | None
    red_dq: str
    red_surrogate: str
    blue_1: str
    blue_2: str
    blue_3: str | None
    blue_dq: str
    blue_surrogate: str
    winner: MatchWinner | None
    time: int
    predicted_time: int | None

    # Red Breakdown
    red_score: int | None
    red_no_foul_points: int | None
    red_foul_points: int | None
    red_auto_points: int | None
    red_teleop_points: int | None
    red_endgame_points: int | None
    red_endgame_1: int | None
    red_endgame_2: int | None
    red_endgame_3: int | None
    red_rp_1: bool | None
    red_rp_2: bool | None
    red_rp_3: bool | None
    red_tiebreaker: int | None
    red_comp_1: float | None
    red_comp_2: float | None
    red_comp_3: float | None
    red_comp_4: float | None
    red_comp_5: float | None
    red_comp_6: float | None
    red_comp_7: float | None
    red_comp_8: float | None
    red_comp_9: float | None
    red_comp_10: float | None
    red_comp_11: float | None
    red_comp_12: float | None
    red_comp_13: float | None
    red_comp_14: float | None
    red_comp_15: float | None
    red_comp_16: float | None
    red_comp_17: float | None
    red_comp_18: float | None

    #Blue breakdown
    blue_score: int | None
    blue_no_foul_points: int | None
    blue_foul_points: int | None
    blue_auto_points: int | None
    blue_teleop_points: int | None
    blue_endgame_points: int | None
    blue_endgame_1: int | None
    blue_endgame_2: int | None
    blue_endgame_3: int | None
    blue_rp_1: bool | None
    blue_rp_2: bool | None
    blue_rp_3: bool | None
    blue_tiebreaker: int | None
    blue_comp_1: float | None
    blue_comp_2: float | None
    blue_comp_3: float | None
    blue_comp_4: float | None
    blue_comp_5: float | None
    blue_comp_6: float | None
    blue_comp_7: float | None
    blue_comp_8: float | None
    blue_comp_9: float | None
    blue_comp_10: float | None
    blue_comp_11: float | None
    blue_comp_12: float | None
    blue_comp_13: float | None
    blue_comp_14: float | None
    blue_comp_15: float | None
    blue_comp_16: float | None
    blue_comp_17: float | None
    blue_comp_18: float | None

    def __init__(self, match: dict[str, Any], year: int) -> None:

        red_alliance = match["alliances"]["red"]
        blue_alliance = match["alliances"]["blue"]

        red_dqs = red_alliance["dq_team_keys"]
        blue_dqs = blue_alliance["dq_team_keys"]

        red_surrogates = red_alliance["surrogate_team_keys"]
        blue_surrogates = blue_alliance["surrogate_team_keys"]

        # notice we use .get() to return an empty dict instead of directly
        # accessing because a match may not have happened yet and the result
        # might be 0
        red_score = match.get("alliances", {}).get("red", {}).get("score", None)
        blue_score = match.get("alliances", {}).get("blue", {}).get("score", None)

        status = MatchStatus.UPCOMING
        if red_score >= 0 and blue_score >= 0:
            status = MatchStatus.COMPLETED

        raw_winner = match.get("winning_alliance", None)
        winner = None
        if raw_winner is not None:
            winner = MatchWinner(raw_winner)

        self.year = year
        self.event = match["event_key"]
        self.key = match["key"]
        self.match_type = MatchType(match["comp_level"])
        self.set_number = match["set_number"]
        self.match_number = match["match_number"]
        self.status = status
        self.video = get_video(cast(str,match["videos"]))
        self.red_1 = red_alliance["team_keys"][0][3:]
        self.red_2 = red_alliance["team_keys"][1][3:]
        self.red_3 = red_alliance["team_keys"][2][3:]
        self.red_dq = ",".join(t[3:] for t in red_dqs)
        self.red_surrogate = ",".join(t[3:] for t in red_surrogates)
        self.blue_1 = blue_alliance["team_keys"][0][3:]
        self.blue_2 = blue_alliance["team_keys"][1][3:]
        self.blue_3 = blue_alliance["team_keys"][2][3:]
        self.blue_dq = ",".join(t[3:] for t in blue_dqs)
        self.blue_surrogate = ",".join(t[3:] for t in blue_surrogates)
        self.winner = winner
        self.time = get_time_from_int(cast(int,match["time"]))
        self.predicted_time = match["predicted_time"]
        self.red_score = red_score
        self.blue_score = blue_score

        # calcuate breakdown values
        if self.status == MatchStatus.COMPLETED:
            breakdown = match.get("score_breakdown", {})
            self._breakdown(breakdown, BREAKDOWN_MAPPINGS.get(year, {}))

            if self.winner == MatchWinner.NOT_PLAYED:
                self.winner = MatchWinner.TIE

            # calculate non penalty points
            if self.red_foul_points and self.blue_foul_points:
                self.red_no_foul_points = self.red_score - self.red_foul_points
                self.blue_no_foul_points = self.blue_score - self.blue_foul_points

    def _breakdown(self, breakdown: dict[str, Any], mapping: dict[str, list[str]]) -> None:

        if not mapping or not breakdown:
            return

        for key, info in mapping.items():

            if len(info["path"]) == 0:
                continue

            curr_path = breakdown
            for tag in info["path"]:
                curr_path = curr_path[tag]

            result = info["type"](curr_path) if curr_path is not None else None
            setattr(self, key, result)
