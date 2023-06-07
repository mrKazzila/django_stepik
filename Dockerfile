FROM python:3.11-slim as base
ENV \
    # python
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random

WORKDIR /app/

RUN groupadd -r docker && \
    useradd -m -g docker unprivilegeduser && \
    mkdir -p /home/unprivilegeduser/.local/share/docker && \
    chown -R unprivilegeduser /home/unprivilegeduser


FROM base as poetry
ENV \
    # poetry
    POETRY_VERSION=1.4.2 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="/root/.local/bin:$PATH"

RUN \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    # deps for installing poetry
        curl && \
    # install poetry
    curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION && \
    # cleaning cache
    rm -rf var/cache && \
    rm -rf /var/lib/apt/lists/*


FROM poetry as venv
ENV POETRY_VIRTUALENVS_CREATE=false

COPY ./poetry.lock ./pyproject.toml /app/
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes


FROM venv as build
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    HOME=/home/app \
    APP_HOME=/home/app/web


COPY --from=venv /app/requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && \
    rm -rf tmp \
    mkdir $HOME \
    mrdir $APP_HOME

WORKDIR $APP_HOME
COPY . $APP_HOME

RUN chown -R unprivilegeduser $APP_HOME

USER unprivilegeduser
