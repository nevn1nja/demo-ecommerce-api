# Ecommerce REST API demo

## Quick Start 🚀

For development setup:

- [PYENV](https://github.com/pyenv/pyenv) 2.3.32 or higher
- [Python](https://www.python.org/downloads/) 3.12.1 or higher
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) 1.7.1 or higher

This project uses [SQLAlchemy](http://sqlalche.me) and [Alembic](https://alembic.sqlalchemy.org) for databases.

To build and run the application:

- [Docker](https://www.docker.com/products/docker-desktop/) latest version

# API Application Development Setup

Install python virtual environment and dependencies

```bash
pyenv install 3.12.5
pyenv local 3.12.5
poetry config virtualenvs.in-project true
poetry env use 3.12.5
poetry install --no-root
```

Add a .env.development file with below variables

```
POSTGRES_USER=<user goes here>
POSTGRES_PASSWORD=<password goes here>
POSTGRES_DB=ecommercedb
POSTGRES_HOST=<localhost or db for docker>
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/${POSTGRES_DB}
DEBUG=True
```

## To run in your local environment without Docker

**1.** Change the .env.development `POSTGRES_HOST=localhost`

**2.** Start the docker database server `docker compose up -d db`

**3.** Run the database migrations

```bash
poetry shell
alembic upgrade head
```

**4.** Running the API server locally (hot-reload on file change):

```bash
poetry shell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**TIP!** The swager docs are at http://localhost:8000/docs

## To run tests in your local environment

```
poetry run pytest
```

## To run it in your local environment using Docker

Run the database migrations

1. Change the .env.development `POSTGRES_HOST=db`

```bash
docker compose --profile dev up
```

## Build and Deploy

To simulate the build and deploy process.

Add .env.production file in the application root with below params.

```
POSTGRES_USER=<user goes here>
POSTGRES_PASSWORD=<password goes here>
POSTGRES_DB=<database goes here>
POSTGRES_HOST=<database host goes here>
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/${POSTGRES_DB}
DEBUG=False
APP_ENV=production
```

Build Docker image for production.

```bash
# Build
docker build . -t demo-ecommerce-api-app-prod --no-cache

# simulate running in prod
docker-compose --profile prod up -d
```

**TIP!** If testing in your local run the db in the background by `docker compose up -d db`