from enum import IntEnum, StrEnum
from typing import Self


class MatchWinner(StrEnum):
    """ An enumeration for which alliance won a match.

    Members:
        RED: The red alliance won the match.
        BLUE: The blue alliance won the match.
        TIE: The match ended in a tie.

    """
    RED = "red"
    BLUE = "blue"
    TIE = "tie"
    NOT_PLAYED = ""


class MatchStatus(StrEnum):
    """ An enumeration for if the match has occurred or is upcomming.

    Members:
        UPCOMING: Match has not yet occurred or data has not be fetched.
        COMPLETED: Match has been completed and data has been uploaded.

    """
    UPCOMING = "Upcoming"
    COMPLETED = "Completed"


class MatchType(StrEnum):
    """ An enumeration for the type of match at the event.

    Members:
        INVALID: The match is invalid for some reason.
        QUAL: Qualification Match
        EIGHTH: First round elimination match.
        QUARTER: Second round or quarterfinal elimination match.
        SEMI: Semifinal elimination match.
        FINAL: Finals elimination match.

    """
    INVALID = "invalid"
    QUAL = "qm"
    EIGHTH = "ef"
    QUARTER = "qf"
    SEMI = "sf"
    FINAL = "f"


class EventStatus(StrEnum):
    """ An enumeration for event status.

    Members:
        INVALID: The event is invalid for some reason.
        UPCOMING: The event has not yet happened.
        ONGOING: The event is ongoing.
        COMPLETED: The event is completed.

    """
    INVALID = "Invalid"
    UPCOMING = "Upcoming"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"


class EventType(IntEnum):
    """ An enumeration for event type.

    Members:
        INVALID: The event is invalid for some reason.
        REGIONAL: The event is a traditional regional event.
        DISTRICT: The event is a district qualifying event.
        DISTRICT_CMP: The event is a distict championship event.
        CMP_DIV: The event is a division at the world championship.
        EINSTEIN: The event is the Einstein final at world championship.
        DISTRICT_CMP_DIV: The event is a district championship division.
        OFFSEASON: The event is an offseason event.

    """
    INVALID = -1
    REGIONAL = 0
    DISTRICT = 1
    DISTRICT_CMP = 2
    CMP_DIV = 3
    EINSTEIN = 4
    DISTRICT_CMP_DIV = 5
    OFFSEASON = 99

    @property
    def is_champs(self) -> bool:
        return self in (EventType.CMP_DIV, EventType.EINSTEIN)

    @property
    def not_champs(self) -> bool:
        return self in (EventType.REGIONAL,
                        EventType.DISTRICT,
                        EventType.DISTRICT_CMP,
                        EventType.DISTRICT_CMP_DIV
                        )

    @property
    def is_offseason(self) -> bool:
        return self == EventType.OFFSEASON

    @property
    def is_official(self) -> bool:
        return self not in (EventType.OFFSEASON, EventType.INVALID)

class ClimbEnum(IntEnum):
    """ An enumeration for the different types of climbs.

    Members:
        NONE: No climb. 0 points.
        PARKED: Robot is parked on the field. 2 points.
        SHALLOWCAGE: Robot is in the shallow cage. 6 points.
        DEEPCAGE: Robot is in the deep cage. 12 points.

    """
    NONE = 0
    PARKED = 2
    SHALLOW_CAGE = 6
    DEEP_CAGE = 12

    @classmethod
    def from_string(cls, value: str) -> Self:
        mapping = {
            "PARKED": cls.PARKED,
            "SHALLOWCAGE": cls.SHALLOW_CAGE,
            "DEEPCAGE": cls.DEEP_CAGE,

        }
        return mapping.get(value.upper(), cls.NONE)

class YesNo(IntEnum):
    """ An enumeration for yes/no values.

    Members:
        NO: No. 0 points.
        YES: Yes. 1 point.
    """
    NO = 0
    YES = 1

    @classmethod
    def from_string(cls, value: str) -> Self:
        """ Convert a string to a YesNo enum. """
        if value.upper() == "YES":
            return cls.YES
        return cls.NO
