FROM python:3.11-slim as prepare

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
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="/root/.local/bin:$PATH"


RUN \
    # update server
    apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps for installing poetry
        curl \
    # install poetry
    && curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION \
    && rm -rf var/cache


WORKDIR /app
COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry export --format requirements.txt --output requirements.txt --without-hashes


FROM poetry as bould

COPY --from=prepare ./app/requirements.txt ./
COPY . ./app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && adduser storeuser \
    && chown -R storeuser:storeuser /app

USER storeuser
