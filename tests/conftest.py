from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from app import app_factory

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aiohttp.web_app import Application
    from pytest_aiohttp.plugin import AiohttpClient


# NOTE: pytest-asyncio 1.x gives every test its own event loop, and an aiohttp
# Application binds to the first loop that touches it, so this fixture must
# stay function-scoped: a session-scoped app raises
# "web.Application instance initialized with different loop" on the second test.
@pytest.fixture(name="app")
def app_fixture() -> Application:
    """Prepare default web app."""
    return app_factory()


@pytest.fixture(autouse=True)
def _stub_bot_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stub the Telegram availability check so tests never hit the network."""

    async def bot_is_available_stub(_: object) -> bool:
        return True

    monkeypatch.setattr(
        "app.core.handlers.health.bot_is_available",
        bot_is_available_stub,
    )


@pytest.fixture(name="http_client")
async def http_client_fixture(
    app: Application,
    aiohttp_client: AiohttpClient,
) -> ClientSession:
    """Prepare client session for app."""
    client = await aiohttp_client(app)

    yield client

    await client.close()

    # Wait 250 ms for the underlying SSL connections to close
    # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
    await asyncio.sleep(0.25)
