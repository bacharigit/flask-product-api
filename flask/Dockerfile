
FROM python:3.12-slim AS base

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


COPY requirements.txt .

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip  install --no-cache-dir  --upgrade pip \
    && /opt/venv/bin/pip  install --no-cache-dir  -r requirements.txt

COPY . .

RUN useradd --create-home  --uid 10001 appuser \
    && chown -R appuser:appuser  /app


FROM base AS test

USER root

COPY requirements-dev.txt  .

RUN /opt/venv/bin/pip install --no-cache-dir -r requirements-dev.txt  

USER appuser

CMD ["pytest"]


FROM base  AS runtime

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
