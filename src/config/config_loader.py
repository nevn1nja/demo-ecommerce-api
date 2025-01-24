import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from src.utils.logger import logger

logger.info("Loading env variables...")
load_dotenv()

env_name = os.getenv("APP_ENV", "development")
env_file = f".env.{env_name}"
logger.info(f"Loading environment variables from: {env_file}")
load_dotenv(env_file)


class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = None
    postgres_db: str = "postgres_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    def get_database_url(self) -> str:
        return (f"postgresql://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")

    debug: bool = False
