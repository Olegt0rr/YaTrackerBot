from collections.abc import Awaitable, Callable
from typing import Any, cast

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from yatracker import YaTracker


class TrackerMiddleware(BaseMiddleware):
    def __init__(self, client: YaTracker) -> None:
        self._client = client

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Add tracker client to Telegram handlers."""
        data["tracker"] = self._client
        message = cast(Message, event)
        return await handler(message, data)
