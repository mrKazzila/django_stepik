FROM python:3.11-slim as base
ENV \
    # python
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random

WORKDIR /var/store/web/

RUN groupadd -r docker && \
    useradd --create-home --gid docker unprivilegeduser && \
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

COPY ./poetry.lock ./pyproject.toml /var/store/web/
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes


FROM venv as build
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --from=venv /var/store/web/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

USER unprivilegeduser

COPY . /var/store/web/
