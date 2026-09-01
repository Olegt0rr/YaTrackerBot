# [Unreleased]

### Changed

- Updated dependencies: aiogram 3.1 → 3.31, pydantic 2.3 → 2.13, pydantic-settings 2.2 → 2.15,
  uvloop 0.21 → 0.22; dev tools: ruff 0.13 → 0.16, mypy 1.17 → 2.3,
  pytest 8 → 9, pre-commit 4.3 → 4.6.
- Replaced black with `ruff format` (Makefile, pre-commit, docs updated).
- Migrated from Poetry to [uv](https://docs.astral.sh/uv/): `pyproject.toml` is
  now PEP 621 (`[project]` + `[dependency-groups]`), `poetry.lock` replaced by
  `uv.lock`, Dockerfile installs dependencies with `uv sync --frozen --no-dev`.
- Dropped the nonexistent `dotenv` extra from pydantic (v2 moved dotenv support
  to pydantic-settings).
- Migrated `Bot(parse_mode=...)` to `Bot(default=DefaultBotProperties(parse_mode=...))`
  (removed in aiogram 3.7).
- Migrated the issue-key filter from the deprecated magic-filter `search=True`
  to `mode=RegexpMode.SEARCH`.
- Python requirement narrowed to `>=3.10,<3.13` (yatracker pins msgspec 0.18,
  which does not support 3.13+).
- Pinned aiosignal to `~1.3` (1.4 typing is incompatible with aiohttp < 3.12,
  and yatracker caps aiohttp below 3.10).
- Migrated ruff configuration to the `[tool.ruff.lint]` layout; refreshed
  pre-commit hooks (ruff, mypy) to match the new tool versions.

### Fixed

- Health checks always returned `UP` even when the bot was unavailable
  (`all(results.items())` → `all(results.values())`).
- Polling no longer overwrites aiohttp's SIGINT/SIGTERM handlers
  (`handle_signals=False`), so graceful web-app shutdown works again.
- Polling shutdown now uses `Dispatcher.stop_polling()` and awaits the polling
  task instead of abandoning it mid-cancel.
- The issue handler no longer tries to send an empty message when every
  tracker lookup fails.
- uvloop is now actually used: the web app runs on a uvloop event loop where
  available (previously the dependency was declared but never activated).
- A polling task that dies on startup is now logged instead of breaking the
  shutdown chain.
- `BaseClient` (health check) now uses aiohttp's default connector: TLS
  certificates are validated again (a bare `ssl.SSLContext()` silently disabled
  verification), and the `ssl_context=` kwarg removed in aiohttp 3.10 is gone.
