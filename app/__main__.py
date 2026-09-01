import logging

from aiohttp.web import run_app

from app import app_factory
from app.core.settings import WebAppSettings

try:
    from uvloop import new_event_loop
except ImportError:  # uvloop is unavailable on Windows and PyPy
    from asyncio import new_event_loop  # type: ignore[assignment]

logging.basicConfig(level=logging.INFO)

settings = WebAppSettings()
app = app_factory()
run_app(
    app,
    host=settings.HOST,
    port=settings.PORT,
    access_log=None,
    loop=new_event_loop(),
)
