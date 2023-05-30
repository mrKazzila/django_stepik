FROM python:3.11-slim as poetry

ENV \
    # python:
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.4.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

WORKDIR /app

COPY . ./

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
    \
    # install poetry
    && curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION \
    && export PATH="/root/.local/bin:$PATH" \
    && poetry --version \
    && poetry export --format requirements.txt --output requirements.txt --without-hashes \
    && rm -rf var/cache


FROM poetry as venv

COPY --from=poetry ./app ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && adduser storeuser \
    && chown -R storeuser:storeuser /app

USER storeuser
