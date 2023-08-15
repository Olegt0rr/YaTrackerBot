from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiogram.fsm.storage.memory import MemoryStorage

if TYPE_CHECKING:
    from aiogram.fsm.storage.base import BaseStorage

logger = logging.getLogger(__name__)


def create_storage() -> BaseStorage:
    """Prepare storage for FSM and data bucket."""

    return MemoryStorage()
