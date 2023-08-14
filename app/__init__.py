from aiohttp.web_app import Application

from .core.setup import setup_core
from .telegram.setup import setup_telegram
from .tracker.setup import setup_tracker


def app_factory() -> Application:
    """Create web app.

    Warning! Setup order matters!
    """
    app = Application()

    setup_tracker(app)
    setup_telegram(app)
    setup_core(app)

    return app
