from typing import Any

from .constants import EVENT_BLACKLIST, MATCH_BLACKLIST


def validate_year(year: int) -> int:
    """
    Validates the year for events and matches.
    Year must be between 1992 and 2026.

    RETURNS YEAR FOR PYDANTIC VALIDATION PURPOSES
    """
    if isinstance(year, int) and (year < 1992 or year >= 2026):
        raise ValueError('Year must be between 1992 and 2026')

    return year


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
