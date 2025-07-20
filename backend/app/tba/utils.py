import logging
from typing import Any

from aiohttp import ClientSession as Session
from aiohttp import ClientTimeout as Timeout

from app.core.config import settings
from app.core.valkey import ValkeyCache

from .constants import EVENT_BLACKLIST, MATCH_BLACKLIST

# Headers are specified on the TBA API reference page
# https://www.thebluealliance.com/apidocs/v3/

API_URL = "https://www.thebluealliance.com/api/v3/"
API_KEY = settings.TBA_API_KEY


async def tba_api_call(
        cache: ValkeyCache,
        endpoint: str,
) -> list[dict]:
    """
    This function takes in the url ending for a TBA endpoint and an ETag
    and returns a json file (or None see returns). CACHE NOT IMPLEMENTED.

    Args:

        endpoint (str): The endpoint for accessing the desired data.
        etag (str | None, optional): The ETag for determining if the data at
            the endpoint has expired. Defaults to None.
        cache (bool, optional): NOT IMPLEMENTED. Defaults to True.

    Returns:

        tuple[Any | bool, str | None]:
            If ETag has not expired returns (True, None).
            If request fails returns (False, None).
            If request succeeds returns (json_data, new_etag).
    """
    headers = {"X-TBA-Auth-Key": API_KEY}

    if await cache.exists(endpoint + "_etag") and await cache.exists(endpoint):
        headers["If-None-Match"] = await cache.get_etag(endpoint + "_etag")

    timeout = Timeout(total=60)

    out_json = [{}]

    async with Session(headers=headers, timeout=timeout) as session:
        async with session.get(API_URL + endpoint) as response:

            if response.status == 304:
                out_json = await cache.get_json(endpoint)
            elif response.status == 200:
                out_json = await response.json()
                etag = response.headers["ETag"]
                await cache.set_json(endpoint, out_json)
                await cache.set_etag(endpoint + "_etag", etag)
            else:
                logging.warning(
                    f"Request to TBA API failed with status code {response.status}"
                    " for endpoint {endpoint}."
                )

    return out_json



def validate_year(year: int) -> int:
    """
    Validates the year for events and matches.
    Year must be between 1992 and 2026.

    RETURNS YEAR FOR PYDANTIC VALIDATION PURPOSES
    """
    if isinstance(year, int) and (year < 1992 or year > 2026):
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
