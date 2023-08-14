from __future__ import annotations

from typing import TYPE_CHECKING

from . import handle_issue, start

if TYPE_CHECKING:
    from aiogram import Dispatcher


def setup(dispatcher: Dispatcher) -> None:
    """Set up handlers."""
    start.setup(dispatcher)
    handle_issue.setup(dispatcher)
