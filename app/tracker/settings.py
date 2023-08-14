from functools import cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class TrackerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TRACKER_")

    ORG_ID: int
    TOKEN: SecretStr


@cache
def get_tracker_settings() -> TrackerSettings:
    """Get cached version of Tracker settings."""
    return TrackerSettings()
