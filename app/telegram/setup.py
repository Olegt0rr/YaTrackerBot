from __future__ import annotations

import asyncio
import logging
from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from app.tracker.setup import TRACKER_APP

from .bot import create_bot
from .dispatcher import create_dispatcher
from .middlewares.tracker import TrackerMiddleware
from .settings import get_telegram_settings
from .storage import create_storage

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher
    from aiogram.fsm.storage.base import BaseStorage
    from aiohttp.web_app import Application
    from yatracker import YaTracker

logger = logging.getLogger(__name__)


def setup_telegram(app: Application) -> None:
    """Set up app for receiving Telegram updates."""
    settings = get_telegram_settings()

    bot = app["bot"] = create_bot()
    storage = app["storage"] = create_storage()
    dispatcher = app["dispatcher"] = create_dispatcher(storage)
    tracker: YaTracker = app[TRACKER_APP]

    dispatcher.message.middleware(TrackerMiddleware(tracker))

    if settings.WEBHOOK_ENABLED:
        handler = SimpleRequestHandler(dispatcher=dispatcher, bot=bot)
        handler.register(app, path=settings.WEBHOOK_PATH)
    else:
        app.on_startup.append(start_polling)
        app.on_shutdown.append(stop_polling)

    app.on_shutdown.append(close_storage)


async def start_polling(app: Application) -> None:
    """Start Telegram polling on app startup."""
    dispatcher: Dispatcher = app["dispatcher"]
    bot: Bot = app["bot"]
    # handle_signals=False: aiogram would otherwise overwrite the SIGINT/SIGTERM
    # handlers installed by aiohttp's run_app, breaking graceful web shutdown.
    polling_coroutine = dispatcher.start_polling(bot, handle_signals=False)
    app["polling_task"] = asyncio.create_task(polling_coroutine)


async def stop_polling(app: Application) -> None:
    """Stop Telegram polling on app shutdown."""
    dispatcher: Dispatcher = app["dispatcher"]
    polling_task: asyncio.Task[None] = app["polling_task"]
    try:
        await dispatcher.stop_polling()
    except RuntimeError:
        # Polling never started (e.g. it crashed on startup) — cancel the task.
        polling_task.cancel()
    with suppress(asyncio.CancelledError):
        try:
            await polling_task
        except Exception:  # a dead poller must not break the shutdown chain
            logger.exception("Polling task failed.")


async def close_storage(app: Application) -> None:
    """Graceful storage close."""
    storage: BaseStorage = app["storage"]
    await storage.close()
