from __future__ import annotations

import asyncio
import json as jsonlib
import logging
from typing import TYPE_CHECKING, Any

import backoff
from aiohttp import BytesPayload, ClientError, ClientSession

if TYPE_CHECKING:
    from collections.abc import Mapping

    from yarl import URL


class BaseClient:
    """Represents base API client."""

    def __init__(self, base_url: str | URL) -> None:
        self._base_url = base_url
        self._session: ClientSession | None = None
        self.log = logging.getLogger(self.__class__.__name__)

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None:
            # The default connector validates TLS certificates; the previous
            # hand-rolled ssl.SSLContext() silently disabled verification and
            # relied on the ssl_context= kwarg removed in aiohttp 3.10.
            self._session = ClientSession(base_url=self._base_url)

        return self._session

    @backoff.on_exception(backoff.expo, ClientError, max_time=60)
    async def _make_request(
        self,
        method: str,
        url: str | URL,
        params: Mapping[str, str] | None = None,
        json: Mapping[str, str] | None = None,
    ) -> tuple[int, dict[str, Any]]:
        """Make request and return decoded json response."""
        session = await self._get_session()

        self.log.debug(
            "Making request %r %r with json %r and params %r",
            method,
            url,
            json,
            params,
        )
        bytes_payload = BytesPayload(
            value=jsonlib.dumps(json).encode(),
            content_type="application/json",
        )

        async with session.request(
            method,
            url,
            params=params,
            data=bytes_payload,
        ) as response:
            status = response.status
            result = await response.json()

        self.log.debug(
            "Got response %r %r with status %r and json %r",
            method,
            url,
            status,
            result,
        )
        return status, result

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            self.log.debug("There's not session to close.")
            return

        if self._session.closed:
            self.log.debug("Session already closed.")
            return

        await self._session.close()
        self.log.debug("Session successfully closed.")

        # Wait 250 ms for the underlying SSL connections to close
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)
