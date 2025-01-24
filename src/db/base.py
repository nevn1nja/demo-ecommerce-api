from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config_loader import Settings
from src.utils.logger import logger

logger.info("Initializing database connection...")

settings = Settings()

SQLALCHEMY_DATABASE_URL = settings.get_database_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
