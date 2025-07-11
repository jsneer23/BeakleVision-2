import time
from datetime import datetime
from typing import Any

from app.tba.constants import (
    DISTRICT_MAPPING,
    EVENT_BLACKLIST,
    MATCH_BLACKLIST,
    PROV_MAPPING,
    STATE_MAPPING,
)


def get_date_from_str(date: str):
    return int(time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple()))


def get_state_prov(state: str) -> str | None:

    if state in STATE_MAPPING:
        return STATE_MAPPING[state]

    if state in STATE_MAPPING.values():
        return state


    if state in PROV_MAPPING:
        return PROV_MAPPING[state]

    if state in PROV_MAPPING.values():
        return state

    return None


def get_district(district: str) -> str | None:

    if district in DISTRICT_MAPPING or district in DISTRICT_MAPPING.values():
        return DISTRICT_MAPPING[district]
    return None


def get_video(website: Any) -> str:  # noqa: ARG001
    """
    NOT IMPLEMENTED
    """
    return ""


def valid_event(event: Any) -> bool:

    event_int = int(event["event_type"])

    if event_int < 0 or event_int > 99:
        return False

    key: str = event["key"]

    if "tempclone" in key or key in EVENT_BLACKLIST:
        return False

    return True

def valid_match(match: Any) -> bool:
    """
    Checks if the match is valid.
    """
    if match["key"] in MATCH_BLACKLIST:
        return False

    return True


def get_time_from_int(time: int) -> Any:  # noqa: ARG001
    return time
