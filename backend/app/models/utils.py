from app.tba.constants import (
    DISTRICT_MAPPING,
    STATE_PROV_MAPPING,
)


def strip_string(value: str | None) -> str | None:
    """Utility function to strip whitespace from a string."""
    return value.strip() if value else None


def get_state_prov(state: str | None) -> str:

    if not isinstance(state, str):
        return ""

    state = state.strip().upper()

    if state in STATE_PROV_MAPPING:
        return STATE_PROV_MAPPING[state]

    return ""


def get_district(district: str | None) -> str:

    if not isinstance(district, str):
        return ""

    district = district.strip().lower()

    if district in DISTRICT_MAPPING or district in DISTRICT_MAPPING.values():
        return DISTRICT_MAPPING[district]

    return ""
