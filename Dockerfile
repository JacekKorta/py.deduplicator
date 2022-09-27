FROM python:3.10 as builder

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.1

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate && poetry install --no-dev --no-root

COPY . ./
RUN . /venv/bin/activate && poetry install

FROM python:3.10.7-alpine3.15
COPY --from=builder /venv /venv
COPY --from=builder /src /src
COPY start.sh ./
ENV PATH="/venv/bin:$PATH"
CMD ["python", "/src/main.py"]
