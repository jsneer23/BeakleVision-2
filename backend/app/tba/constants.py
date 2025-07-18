from enum import IntEnum, StrEnum
from typing import Any, Self


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


class District(StrEnum):
    """ An enumeration for FRC districts. """
    FNC = "North Carolina"
    FIT = "Texas"
    FIN = "Indiana"
    FMA = "Mid-Atlantic"
    CHS = "Chesapeake"
    FIM = "Michigan"
    FSC = "South Carolina"
    PCH = "Peachtree"
    PNW = "Pacific Northwest"
    ISR = "Israel"
    ONT = "Ontario"
    NE = "New England"
    NA = ""


class StateProv(StrEnum):
    """ An enumeration for US states and Canadian provinces. """
    AL = "Alabama"
    AK = "Alaska"
    AS = "American Samoa"
    AZ = "Arizona"
    AR = "Arkansas"
    CA = "California"
    CO = "Colorado"
    CT = "Connecticut"
    DE = "Delaware"
    DC = "District of Columbia"
    FL = "Florida"
    GA = "Georgia"
    GU = "Guam"
    HI = "Hawaii"
    ID = "Idaho"
    IL = "Illinois"
    IN = "Indiana"
    IA = "Iowa"
    KS = "Kansas"
    KY = "Kentucky"
    LA = "Louisiana"
    ME = "Maine"
    MD = "Maryland"
    MA = "Massachusetts"
    MI = "Michigan"
    MN = "Minnesota"
    MS = "Mississippi"
    MO = "Missouri"
    MT = "Montana"
    NE = "Nebraska"
    NV = "Nevada"
    NH = "New Hampshire"
    NJ = "New Jersey"
    NM = "New Mexico"
    NY = "New York"
    NC = "North Carolina"
    ND = "North Dakota"
    MP = "Northern Mariana Islands"
    OH = "Ohio"
    OK = "Oklahoma"
    OR = "Oregon"
    PA = "Pennsylvania"
    PR = "Puerto Rico"
    RI = "Rhode Island"
    SC = "South Carolina"
    SD = "South Dakota"
    TN = "Tennessee"
    TX = "Texas"
    UT = "Utah"
    VT = "Vermont"
    VI = "Virgin Islands"
    VA = "Virginia"
    WA = "Washington"
    WV = "West Virginia"
    WI = "Wisconsin"
    WY = "Wyoming"
    NL = "Newfoundland"
    PE = "Prince Edward Island"
    NS = "Nova Scotia"
    NB = "New Brunswick"
    QC = "Québec"
    ON = "Ontario"
    MB = "Manitoba"
    SK = "Saskatchewan"
    AB = "Alberta"
    BC = "British Columbia"
    YT = "Yukon"
    NT = "Northwest Territories"
    NU = "Nunavut"
    NA = ""

STATE_PROV_MAPPING: dict[str, str] = {
    "AL": "Alabama",
    "ALABAMA": "Alabama",
    "AK": "Alaska",
    "ALASKA": "Alaska",
    "AS": "American Samoa",
    "AMERICAN SAMOA": "American Samoa",
    "AZ": "Arizona",
    "ARIZONA": "Arizona",
    "AR": "Arkansas",
    "ARKANSAS": "Arkansas",
    "CA": "California",
    "CALIFORNIA": "California",
    "CO": "Colorado",
    "COLORADO": "Colorado",
    "CT": "Connecticut",
    "CONNECTICUT": "Connecticut",
    "DE": "Delaware",
    "DELAWARE": "Delaware",
    "DC": "District of Columbia",
    "DISTRICT OF COLUMBIA": "District of Columbia",
    "FL": "Florida",
    "FLORIDA": "Florida",
    "GA": "Georgia",
    "GEORGIA": "Georgia",
    "GU": "Guam",
    "GUAM": "Guam",
    "HI": "Hawaii",
    "HAWAII": "Hawaii",
    "ID": "Idaho",
    "IDAHO": "Idaho",
    "IL": "Illinois",
    "ILLINOIS": "Illinois",
    "IN": "Indiana",
    "INDIANA": "Indiana",
    "IA": "Iowa",
    "IOWA": "Iowa",
    "KS": "Kansas",
    "KANSAS": "Kansas",
    "KY": "Kentucky",
    "KENTUCKY": "Kentucky",
    "LA": "Louisiana",
    "LOUISIANA": "Louisiana",
    "ME": "Maine",
    "MAINE": "Maine",
    "MD": "Maryland",
    "MARYLAND": "Maryland",
    "MA": "Massachusetts",
    "MASSACHUSETTS": "Massachusetts",
    "MI": "Michigan",
    "MICHIGAN": "Michigan",
    "MN": "Minnesota",
    "MINNESOTA": "Minnesota",
    "MS": "Mississippi",
    "MISSISSIPPI": "Mississippi",
    "MO": "Missouri",
    "MISSOURI": "Missouri",
    "MT": "Montana",
    "MONTANA": "Montana",
    "NE": "Nebraska",
    "NEBRASKA": "Nebraska",
    "NV": "Nevada",
    "NEVADA": "Nevada",
    "NH": "New Hampshire",
    "NEW HAMPSHIRE": "New Hampshire",
    "NJ": "New Jersey",
    "NEW JERSEY": "New Jersey",
    "NM": "New Mexico",
    "NEW MEXICO": "New Mexico",
    "NY": "New York",
    "NEW YORK": "New York",
    "NC": "North Carolina",
    "NORTH CAROLINA": "North Carolina",
    "ND": "North Dakota",
    "NORTH DAKOTA": "North Dakota",
    "MP": "Northern Mariana Islands",
    "NORTHERN MARIANA ISLANDS": "Northern Mariana Islands",
    "OH": "Ohio",
    "OHIO": "Ohio",
    "OK": "Oklahoma",
    "OKLAHOMA": "Oklahoma",
    "OR": "Oregon",
    "OREGON": "Oregon",
    "PA": "Pennsylvania",
    "PENNSYLVANIA": "Pennsylvania",
    "PR": "Puerto Rico",
    "PUERTO RICO": "Puerto Rico",
    "RI": "Rhode Island",
    "RHODE ISLAND": "Rhode Island",
    "SC": "South Carolina",
    "SOUTH CAROLINA": "South Carolina",
    "SD": "South Dakota",
    "SOUTH DAKOTA": "South Dakota",
    "TN": "Tennessee",
    "TENNESSEE": "Tennessee",
    "TX": "Texas",
    "TEXAS": "Texas",
    "UT": "Utah",
    "UTAH": "Utah",
    "VT": "Vermont",
    "VERMONT": "Vermont",
    "VI": "Virgin Islands",
    "VIRGIN ISLANDS": "Virgin Islands",
    "VA": "Virginia",
    "VIRGINIA": "Virginia",
    "WA": "Washington",
    "WASHINGTON": "Washington",
    "WV": "West Virginia",
    "WEST VIRGINIA": "West Virginia",
    "WI": "Wisconsin",
    "WISCONSIN": "Wisconsin",
    "WY": "Wyoming",
    "WYOMING": "Wyoming",
    "NL": "Newfoundland",
    "NEWFOUNDLAND": "Newfoundland",
    "PE": "Prince Edward Island",
    "PRINCE EDWARD ISLAND": "Prince Edward Island",
    "NS": "Nova Scotia",
    "NOVA SCOTIA": "Nova Scotia",
    "NB": "New Brunswick",
    "NEW BRUNSWICK": "New Brunswick",
    "QC": "Québec",
    "QUEBEC": "Québec",
    "QUÉBEC": "Québec",
    "ON": "Ontario",
    "ONTARIO": "Ontario",
    "MB": "Manitoba",
    "MANITOBA": "Manitoba",
    "SK": "Saskatchewan",
    "SASKATCHEWAN": "Saskatchewan",
    "AB": "Alberta",
    "ALBERTA": "Alberta",
    "BC": "British Columbia",
    "BRITISH COLUMBIA": "British Columbia",
    "YT": "Yukon",
    "YUKON": "Yukon",
    "NT": "Northwest Territories",
    "NORTHWEST TERRITORIES": "Northwest Territories",
    "NU": "Nunavut",
    "NUNAVUT": "Nunavut",
}


DISTRICT_MAPPING: dict[str, str] = {
    "nc": "North Carolina",
    "fnc": "North Carolina",
    "tx": "Texas",
    "fit": "Texas",
    "in": "Indiana",
    "fin": "Indiana",
    "mar": "Mid-Atlantic",
    "fma": "Mid-Atlantic",
    "chs": "Chesapeake",
    "fim": "Michigan",
    "fsc": "South Carolina",
    "pch": "Peachtree",
    "pnw": "Pacific Northwest",
    "isr": "Israel",
    "ont": "Ontario",
    "ne": "New England",
}


EVENT_BLACKLIST: list[str] = [
    "2004va",
    "2005va",
    "2007ga",
    "2022zhha",
    "2024nywz",
]


MATCH_BLACKLIST: list[str] = []


BREAKDOWN_MAPPINGS: dict[int, dict[str, dict[str, Any]]] = {
    2025: {
        "red_foul_points": {"path": ["red", "foulPoints"], "type": int},
        "red_auto_points": {"path": ["red", "autoPoints"], "type": int},
        "red_teleop_points": {"path": ["red", "teleopPoints"], "type": int},
        "red_endgame_points": {"path": ["red", "endGameBargePoints"], "type": int},
        "red_endgame_1": {"path": ["red", "endGameRobot1"], "type": ClimbEnum.from_string},
        "red_endgame_2": {"path": ["red", "endGameRobot2"], "type": ClimbEnum.from_string},
        "red_endgame_3": {"path": ["red", "endGameRobot3"], "type": ClimbEnum.from_string},
        "red_rp_1": {"path": ["red", "autoBonusAchieved"], "type": int},
        "red_rp_2": {"path": ["red", "coralBonusAchieved"], "type": int},
        "red_rp_3": {"path": ["red", "bargeBonusAchieved"], "type": int},
        "red_comp_1": {"path": ["red", "autoLineRobot1"], "type": YesNo.from_string},
        "red_comp_2": {"path": ["red", "autoLineRobot2"], "type": YesNo.from_string},
        "red_comp_3": {"path": ["red", "autoLineRobot3"], "type": YesNo.from_string},
        "red_comp_4": {"path": ["red", "autoReef", "tba_topRowCount"], "type": int},
        "red_comp_5": {"path": ["red", "autoReef", "tba_midRowCount"], "type": int},
        "red_comp_6": {"path": ["red", "autoReef", "tba_botRowCount"], "type": int},
        'red_comp_7': {"path": ["red", "teleopReef", "trough"], "type": int},
        "red_comp_8": {"path": ["red", "teleopReef", "tba_topRowCount"], "type": int},
        "red_comp_9": {"path": ["red", "teleopReef", "tba_midRowCount"], "type": int},
        "red_comp_10": {"path": ["red", "teleopReef", "tba_botRowCount"], "type": int},
        "red_comp_11": {"path": ["red", "teleopReef", "trough"], "type": int},
        "red_comp_12": {"path": ["red", "netAlgaeCount"], "type": int},
        "red_comp_13": {"path": ["red", "wallAlgaeCount"], "type": int},
        "red_comp_14": {"path": ["red", "coopertitionCriteriaMet"], "type": int},
        "red_comp_15": {"path": [], "type": int},
        "red_comp_16": {"path": [], "type": int},
        "red_comp_17": {"path": [], "type": int},
        "red_comp_18": {"path": [], "type": int},
        "blue_foul_points": {"path": ["blue", "foulPoints"], "type": int},
        "blue_auto_points": {"path": ["blue", "autoPoints"], "type": int},
        "blue_teleop_points": {"path": ["blue", "teleopPoints"], "type": int},
        "blue_endgame_points": {"path": ["blue", "endGameBargePoints"], "type": int},
        "blue_endgame_1": {"path": ["blue", "endGameRobot1"], "type": ClimbEnum.from_string},
        "blue_endgame_2": {"path": ["blue", "endGameRobot2"], "type": ClimbEnum.from_string},
        "blue_endgame_3": {"path": ["blue", "endGameRobot3"], "type": ClimbEnum.from_string},
        "blue_rp_1": {"path": ["blue", "autoBonusAchieved"], "type": int},
        "blue_rp_2": {"path": ["blue", "coralBonusAchieved"], "type": int},
        "blue_rp_3": {"path": ["blue", "bargeBonusAchieved"], "type": int},
        "blue_comp_1": {"path": ["blue", "autoLineRobot1"], "type": YesNo.from_string},
        "blue_comp_2": {"path": ["blue", "autoLineRobot2"], "type": YesNo.from_string},
        "blue_comp_3": {"path": ["blue", "autoLineRobot3"], "type": YesNo.from_string},
        "blue_comp_4": {"path": ["blue", "autoReef", "tba_topRowCount"], "type": int},
        "blue_comp_5": {"path": ["blue", "autoReef", "tba_midRowCount"], "type": int},
        "blue_comp_6": {"path": ["blue", "autoReef", "tba_botRowCount"], "type": int},
        'blue_comp_7': {"path": ["blue", "teleopReef", "trough"], "type": int},
        "blue_comp_8": {"path": ["blue", "teleopReef", "tba_topRowCount"], "type": int},
        "blue_comp_9": {"path": ["blue", "teleopReef", "tba_midRowCount"], "type": int},
        "blue_comp_10": {"path": ["blue", "teleopReef", "tba_botRowCount"], "type": int},
        "blue_comp_11": {"path": ["blue", "teleopReef", "trough"], "type": int},
        "blue_comp_12": {"path": ["blue", "netAlgaeCount"], "type": int},
        "blue_comp_13": {"path": ["blue", "wallAlgaeCount"], "type": int},
        "blue_comp_14": {"path": ["blue", "coopertitionCriteriaMet"], "type": int},
        "blue_comp_15": {"path": [], "type": int},
        "blue_comp_16": {"path": [], "type": int},
        "blue_comp_17": {"path": [], "type": int},
        "blue_comp_18": {"path": [], "type": int}
    }
}
