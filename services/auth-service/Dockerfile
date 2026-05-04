# Base
FROM python:3.11-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Runtime Dependencies Stage
FROM base AS deps-prod

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Development Dependencies Stage
FROM base AS deps-dev

COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Test Stage
FROM deps-dev AS test

COPY . .

ENV JWT_SECRET=jwt_secret_test

RUN pytest --cov=app

# Runtime Stage
FROM deps-prod AS runtime

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]