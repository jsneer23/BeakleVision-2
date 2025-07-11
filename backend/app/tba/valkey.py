import logging
from types import TracebackType
from typing import Any, Self

import orjson
import valkey.exceptions as valkey_exceptions
from valkey.asyncio import ConnectionPool, Valkey

from app.core.config import settings


class ValkeyCache:

    def __init__(self, url):
        pool = ConnectionPool.from_url(url)
        self.client = Valkey(connection_pool=pool)

    async def __aenter__(self) -> Self:
        print("Connecting to Valkey...")
        return self

    async def __aexit__(
            self,
            exc_type: type[valkey_exceptions.ValkeyError] | None,
            exc: valkey_exceptions.ValkeyError | None,
            traceback: TracebackType | None,
    ) -> None:
        await self.client.aclose(close_connection_pool=True)


    async def set(self, endpoint: str, data: dict[str, Any]) -> None:

        try:
            await self.client.set(endpoint, orjson.dumps(data))
        except ConnectionError:
            logging.warning("Could not connect to Valkey. "
                            "Data not stored in cache.")


    async def get(self, endpoint: str) -> dict[str, Any] | bool:

        out = False

        try:
            cached_data: bytes | None = await self.client.get(endpoint)
            if type(cached_data) is bytes:
                out = orjson.loads(cached_data.decode('UTF-8'))
        except valkey_exceptions.ConnectionError:
            logging.warning("Could not connect to Valkey. "
                            "Data not retreived from cache.")

        return out

cache = ValkeyCache(str(settings.VALKEY_URI))
