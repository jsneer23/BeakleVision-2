import logging
from types import TracebackType
from typing import Any, Self

#import orjson
import valkey.exceptions as valkey_exceptions
from valkey.asyncio import ConnectionPool, Valkey
from valkey.commands.json.path import Path

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValkeyCache:

    def __init__(self):
        self.url = str(settings.VALKEY_CACHE_URI)
        pool = ConnectionPool.from_url(self.url, decode_responses=True)
        self.client = Valkey(connection_pool=pool)

    def __enter__(self) -> Self:
        return self

    def __exit__(
            self,
            exc_type: type[valkey_exceptions.ValkeyError] | None,
            exc: valkey_exceptions.ValkeyError | None,
            traceback: TracebackType | None,
    ) -> None:
        pass

    async def set_etag(self, endpoint: str, data: Any) -> None:
        """Set a value in the Valkey cache."""
        try:
            await self.client.set(endpoint, data)
        except valkey_exceptions.ConnectionError:
            logging.warning("Could not connect to Valkey. "
                            "Data not stored in cache.")

    async def set_json(self, endpoint: str, data: dict[str, Any]) -> None:
        """Set a JSON value in the Valkey cache."""
        try:
            #await self.client.set(endpoint, orjson.dumps(data))
            await self.client.json().set(endpoint, Path.root_path(), data)
        except valkey_exceptions.ConnectionError:
            logging.warning("Could not connect to Valkey. "
                            "Data not stored in cache.")

    async def get_etag(self, endpoint: str) -> Any | bool:
        """Get a value from the Valkey cache."""
        out = False

        try:
            out = await self.client.get(endpoint)
        except valkey_exceptions.ConnectionError:
            logging.warning("Could not connect to Valkey. "
                            "Data not retreived from cache.")

        return out

    async def get_json(self, endpoint: str) -> dict[str, Any] | bool:
        """Get a JSON value from the Valkey cache."""
        out = False

        try:
            out: dict[str, Any] = await self.client.json().get(endpoint, Path.root_path())
            #cached_data: bytes | None = await self.client.get(endpoint)
            #if type(cached_data) is bytes:
            #    out = orjson.loads(cached_data.decode('UTF-8'))
        except valkey_exceptions.ConnectionError:
            logging.warning("Could not connect to Valkey. "
                            "Data not retreived from cache.")

        return out

    async def exists(self, endpoint_etag: str) -> bool:
        """Check if a key exists in the Valkey cache."""
        try:
            exists = await self.client.exists(endpoint_etag)
            return exists
        except valkey_exceptions.ConnectionError:
            logging.warning("Could not connect to Valkey. "
                            "Existence check failed.")
            return False

    async def delete(self, endpoint_etag: str) -> None:
        """Delete a key from the Valkey cache."""
        try:
            await self.client.delete(endpoint_etag)
        except valkey_exceptions.ConnectionError:
            logging.warning("Could not connect to Valkey. "
                            "Deletion failed.")

    async def close(self) -> None:
        """Close the Valkey connection pool."""
        await self.client.aclose(close_connection_pool=True)
        logger.info("Valkey Connection Pool closed.")

valkey_cache = ValkeyCache()
