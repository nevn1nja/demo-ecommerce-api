import os
from unittest.mock import patch

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from main import app
from src.config.config_loader import Settings
from src.db.base import get_db

TEST_DB_FILE = "test_ecommerce.db"
TEST_SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ALEMBIC_CONFIG_PATH = "alembic.ini"


@pytest.fixture(scope="session", autouse=True)
def mock_get_database_url():
    with patch.object(Settings, "get_database_url", return_value=TEST_SQLALCHEMY_DATABASE_URL):
        yield TEST_SQLALCHEMY_DATABASE_URL


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(mock_get_database_url):
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    alembic_cfg = Config(ALEMBIC_CONFIG_PATH)
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_SQLALCHEMY_DATABASE_URL)
    alembic_cfg.set_main_option("script_location",
                                "alembic")  # Adjust if needed

    command.upgrade(alembic_cfg, "head")
    yield

    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


@pytest.fixture
def mock_db(apply_migrations):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
