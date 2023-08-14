import html

from aiogram.utils.markdown import hbold
from yatracker.types import FullIssue


def get_issue_preview(issue: FullIssue) -> str:
    """Get issue preview text."""
    lines: list[str] = [
        hbold(issue.key),
        html.escape(issue.summary),
        f"Статус: {issue.status.display}",
    ]

    if issue.assignee is not None:
        assignee = f"Ответственный: {issue.assignee.display}"
        lines.append(assignee)

    return "\n".join(lines)
