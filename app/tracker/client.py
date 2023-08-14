import logging

from yatracker import YaTracker

from .settings import get_tracker_settings

logger = logging.getLogger(__name__)


def create_tracker() -> YaTracker:
    """Create Tracker client."""
    _settings = get_tracker_settings()
    client = YaTracker(
        org_id=_settings.ORG_ID,
        token=_settings.TOKEN.get_secret_value(),
    )
    logger.debug("Yandex Tracker client created.")
    return client
