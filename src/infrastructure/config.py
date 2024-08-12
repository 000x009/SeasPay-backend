import os
from dataclasses import dataclass


@dataclass
class BaseDB:
    "Base database config"

    host: str
    db_name: str
    user: str
    password: str

    @property
    def connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}"


@dataclass
class DB(BaseDB):
    """App database config"""


@dataclass
class Settings:
    """App settings"""

    db: DB


def load_settings() -> Settings:
    """Get app settings"""

    db = DB(
        host=os.environ['DB_PORT'],
        db_name=os.environ['DB_NAME'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
    )

    return Settings(db=db)
