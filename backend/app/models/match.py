from datetime import datetime
from typing import Any

from pydantic import field_validator, model_validator
from sqlmodel import Field, Relationship, SQLModel

from app.tba.constants import (
    BREAKDOWN_MAPPINGS,
    MatchStatus,
    MatchType,
    MatchWinner,
)

from .event import Event


def _breakdown(match_dict: dict[str, Any], mapping: dict[str, list[str]]) -> None:

    breakdown = match_dict.get("score_breakdown", {})

    if not mapping or not breakdown:
        return

    for key, info in mapping.items():

        if len(info["path"]) == 0:
            continue

        curr_path = breakdown
        for tag in info["path"]:
            curr_path = curr_path[tag]

        match_dict[key] = info["type"](curr_path) if curr_path is not None else None


class MatchBase(SQLModel):
    """
    Base Pydantic/SQLModel that holds match information from TBA.

    Each match has a match breakdown that split out into red and blue.

    The breakdown is different for each season. For more info see the TBA API at
    https://www.thebluealliance.com/apidocs/v3 and look at src.tba.breakdown to
    see how the API values are converted into values here.
    """
    year: int
    event_key: str
    key: str

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
    time: datetime
    predicted_time: int | None

    # red breakdown
    red_score: int | None = None
    red_no_foul_points: int | None = None
    red_foul_points: int | None = None
    red_auto_points: int | None = None
    red_teleop_points: int | None = None
    red_endgame_points: int | None = None
    red_endgame_1: int | None = None
    red_endgame_2: int | None = None
    red_endgame_3: int | None = None
    red_rp_1: bool | None = None
    red_rp_2: bool | None = None
    red_rp_3: bool | None = None
    red_comp_1: int | None = None
    red_comp_2: int | None = None
    red_comp_3: int | None = None
    red_comp_4: int | None = None
    red_comp_5: int | None = None
    red_comp_6: int | None = None
    red_comp_7: int | None = None
    red_comp_8: int | None = None
    red_comp_9: int | None = None
    red_comp_10: int | None = None
    red_comp_11: int | None = None
    red_comp_12: int | None = None
    red_comp_13: int | None = None
    red_comp_14: int | None = None
    red_comp_15: int | None = None
    red_comp_16: int | None = None
    red_comp_17: int | None = None
    red_comp_18: int | None = None

    # blue breakdown
    blue_score: int | None = None
    blue_no_foul_points: int | None = None
    blue_foul_points: int | None = None
    blue_auto_points: int | None = None
    blue_teleop_points: int | None = None
    blue_endgame_points: int | None = None
    blue_endgame_1: int | None = None
    blue_endgame_2: int | None = None
    blue_endgame_3: int | None = None
    blue_rp_1: bool | None = None
    blue_rp_2: bool | None = None
    blue_rp_3: bool | None = None
    blue_comp_1: int | None = None
    blue_comp_2: int | None = None
    blue_comp_3: int | None = None
    blue_comp_4: int | None = None
    blue_comp_5: int | None = None
    blue_comp_6: int | None = None
    blue_comp_7: int | None = None
    blue_comp_8: int | None = None
    blue_comp_9: int | None = None
    blue_comp_10: int | None = None
    blue_comp_11: int | None = None
    blue_comp_12: int | None = None
    blue_comp_13: int | None = None
    blue_comp_14: int | None = None
    blue_comp_15: int | None = None
    blue_comp_16: int | None = None
    blue_comp_17: int | None = None
    blue_comp_18: int | None = None


class MatchCreate(MatchBase):

    @model_validator(mode="before")
    @classmethod
    def validate_match(cls, match_dict: dict[str, Any]) -> dict[str, Any]:

        match_dict["year"] = int(match_dict["key"].strip()[:4])

        # Unpack nested json
        red_alliance = match_dict["alliances"]["red"]
        blue_alliance = match_dict["alliances"]["blue"]

        red_dqs = red_alliance["dq_team_keys"]
        blue_dqs = blue_alliance["dq_team_keys"]

        red_surrogates = red_alliance["surrogate_team_keys"]
        blue_surrogates = blue_alliance["surrogate_team_keys"]

        # Put data back so it matches db columns
        match_dict["red_score"] = red_alliance.get("score", None)
        match_dict["blue_score"] = red_alliance.get("score", None)

        match_dict["red_1"] = red_alliance["team_keys"][0][3:]
        match_dict["red_2"] = red_alliance["team_keys"][1][3:]
        match_dict["red_3"] = red_alliance["team_keys"][2][3:]

        match_dict["blue_1"] = blue_alliance["team_keys"][0][3:]
        match_dict["blue_2"] = blue_alliance["team_keys"][1][3:]
        match_dict["blue_3"] = blue_alliance["team_keys"][2][3:]

        match_dict["red_dq"] = ",".join(t[3:] for t in red_dqs)
        match_dict["red_surrogate"] = ",".join(t[3:] for t in red_surrogates)

        match_dict["blue_dq"] = ",".join(t[3:] for t in blue_dqs)
        match_dict["blue_surrogate"] = ",".join(t[3:] for t in blue_surrogates)

        match_dict["winner"] = match_dict.get("winning_alliance", "").lower()

        match_dict["match_type"] = match_dict["comp_level"]

        #TODO Handle match video
        match_dict["video"] = ""

        # determine if match is completed, and if so assign tie if necessary, and calculate non-penalty points
        match_dict["status"] = "Upcoming"
        if match_dict["red_score"] >= 0 and match_dict["blue_score"] >= 0:
            match_dict["status"] = "Completed"

            if match_dict["winner"] == "":
                match_dict["winner"] = "tie"

            # unpack nested breakdown json
            _breakdown(match_dict, BREAKDOWN_MAPPINGS.get(int(match_dict["year"]), {}))

            # calculate non penalty points
            if isinstance(match_dict.get("red_foul_points", None), int) and isinstance(match_dict.get("blue_foul_points", None), int):
                match_dict["red_no_foul_points"] = match_dict["red_score"] - match_dict["red_foul_points"]
                match_dict["blue_no_foul_points"] = match_dict["blue_score"] - match_dict["blue_foul_points"]

        return match_dict


class Match(MatchBase, table=True):
    """
    SQL table that holds match information from TBA
    """
    year: int = Field(foreign_key="yearstats.year")
    event_key: str = Field(foreign_key="event.key")
    key: str = Field(primary_key=True)

    event_info: "Event" = Relationship(back_populates="matches") #3
