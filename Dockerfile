FROM python:3.11-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc as files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    LOCALES_PATH="/opt/locales" \
    APP_PATH="/src"

# prepend venv to path
ENV PATH="$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        # for building python deps without wheels
        build-essential \
    && apt-get clean

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.12.8 /uv /uvx /usr/local/bin/

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY uv.lock pyproject.toml ./

# install runtime deps into $PYSETUP_PATH/.venv from the lock file
RUN uv sync --frozen --no-dev --no-cache


FROM python-base AS production

# vars
ARG APP_ENV=production
ENV APP_ENV=$APP_ENV

# copy generated files (python libs, .mo locales, migrations)
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# copy app files
WORKDIR $APP_PATH
COPY tools/check_health.py ./
COPY app ./app

# good luck! :)
CMD python -m app
