from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

from aiogram import F
from yatracker.exceptions import YaTrackerError

from app.tracker.helpers import get_issue_preview

if TYPE_CHECKING:
    from aiogram import Dispatcher
    from aiogram.types import Message
    from yatracker import YaTracker
    from yatracker.types import FullIssue

ISSUE_PATTERN = re.compile(r"(\w+-\d+)")

logger = logging.getLogger(__name__)


async def handle_issues(
    message: Message,
    tracker: YaTracker,
    issue_pattern: re.Pattern[str] = ISSUE_PATTERN,
) -> None:
    """Handle issue pattern."""
    text = message.text or message.caption or ""
    keys = issue_pattern.findall(text)

    issues: list[FullIssue] = []
    for key in keys:
        try:
            issue = await tracker.get_issue(key)
        except YaTrackerError as exc:
            logger.warning(
                "Can't get %s issue. %s: %s",
                key,
                type(exc).__name__,
                exc,
            )
        else:
            issues.append(issue)

    lines: list[str] = []
    for issue in issues:
        preview = get_issue_preview(issue)
        lines.append(preview)

    await message.answer("\n\n".join(lines))


def setup(dispatcher: Dispatcher) -> None:
    """Register handlers."""
    dispatcher.message.register(
        handle_issues,
        F.text.regexp(r"(\w+-\d+)", search=True),
    )
