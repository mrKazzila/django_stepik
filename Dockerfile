FROM python:3.11-slim as base
ENV \
    # python:
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random

WORKDIR /app

RUN groupadd -r docker && \
    useradd --create-home --gid docker unprivilegeduser && \
    mkdir -p /home/unprivilegeduser/.local/share/docker && \
    chown -R unprivilegeduser /home/unprivilegeduser


FROM base as poetry
ENV \
    # poetry:
    POETRY_VERSION=1.4.2 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="/root/.local/bin:$PATH"

RUN \
    # update server
    apt-get update && \
    apt-get install --no-install-recommends -y \
    # deps for installing poetry
        curl && \
    # install poetry
    curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION && \
    rm -rf var/cache && \
    rm -rf /var/lib/apt/lists/*


FROM poetry as venv
ENV \
    # poetry:
    POETRY_VIRTUALENVS_CREATE=false

COPY ./poetry.lock ./pyproject.toml /app/
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes


FROM venv as build
COPY --from=venv /app/requirements.txt /tmp/requirements.txt

RUN python -m venv .venv && \
    .venv/bin/pip install 'wheel==0.36.2' && \
    .venv/bin/pip install -r /tmp/requirements.txt


FROM python:3.11-slim as runtime
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
ENV PATH=/app/.venv/bin:$PATH

COPY --from=build /app/.venv /app/.venv
COPY . /app
