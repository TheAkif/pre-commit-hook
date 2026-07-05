FROM python:3.10.4-slim-bullseye AS base

WORKDIR /application

# Needed to build/compile psycopg2 (and other Python extensions written in C or C++)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv and have it install packages straight into the system
# interpreter (no virtualenv) so `uvicorn`/`pytest` work without `pipenv run`.
RUN pip install pipenv

# Copy packaging requirements
COPY ./Pipfile ./

ENTRYPOINT ["bash", "./boot.sh"]

###################
# Development
###################
FROM base AS development

# Install dev dependencies as well
RUN pipenv install --system --dev --skip-lock

COPY . .

CMD ["development"]

###################
# Production
###################
FROM base AS production

# Install production dependencies only
RUN pipenv install --system --skip-lock

COPY . .

CMD ["production"]
