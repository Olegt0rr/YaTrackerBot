from __future__ import annotations

from typing import TYPE_CHECKING

from .client import create_tracker

if TYPE_CHECKING:
    from aiohttp.web_app import Application
    from yatracker import YaTracker

TRACKER_APP = "tracker"


def setup_tracker(app: Application) -> None:
    """Set up Tracker client."""
    app[TRACKER_APP] = create_tracker()
    app.on_shutdown.append(_close)


async def _close(app: Application) -> None:
    """Graceful Tracker client close."""
    traker: YaTracker = app[TRACKER_APP]
    await traker.close()
