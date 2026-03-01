FROM python:3.14.3-slim as base

ENV PATH="/venv/bin:$PATH" \
    APP_PATH="/app"

FROM base as build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv venv /venv

WORKDIR $APP_PATH

RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY ./src ./src
COPY pyproject.toml uv.lock ./

RUN uv build --wheel && \
    uv pip install --no-deps dist/*.whl

FROM base as final
COPY --from=build /venv /venv
