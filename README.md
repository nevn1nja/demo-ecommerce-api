# Ecommerce REST API demo

## Quick Start 🚀

For development setup:
- [Python](https://www.python.org/downloads/) 3.12.1 or higher
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) 1.7.1 or higher

This project uses [SQLAlchemy](http://sqlalche.me) and [Alembic](https://alembic.sqlalchemy.org) for databases.


To build and run the application:
- [Docker](https://www.docker.com/products/docker-desktop/) latest version

## For the API Application

Install python virtual environment and dependencies

```bash
poetry config virtualenvs.in-project true
poetry env use 3.11.8
poetry install --no-root
```

## Development Setup

Add a .env file with below variables

```
POSTGRES_USER=Username for dev database
POSTGRES_PASSWORD=Password
POSTGRES_DB=Database
POSTGRES_HOST=db
POSTGRES_PORT=Port
DEBUG=True
```
If you wish to use the database created by docker compose, keep the `POSTGRES_HOST=db` param as is. 

To run the project in local:
Ensure entrypoint.sh has execution permission.
```bash
sudo chmod +x entrypoint.sh
```
```bash
docker-compose --profile dev up
```

## To Run it on localhost without Docker
Run the database migrations
```bash
poetry shell
alembic upgrade head
```

## Running the API Application

Running the API server locally (hot-reload on file change):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Build and deploy
Add .env.production file in the application root with below params.
```
POSTGRES_USER=Username for production DB
POSTGRES_PASSWORD=Password
POSTGRES_DB=Database Name
POSTGRES_HOST=Hostname
POSTGRES_PORT=Port
DEBUG=False
```
Build Docker image for production.
```bash
docker-compose --profile prod
```
