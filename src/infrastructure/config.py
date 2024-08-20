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
class BotSettings:
    bot_token: str


@dataclass
class Settings:
    """App settings"""

    db: DB
    bot: BotSettings


def load_settings() -> Settings:
    """Get app settings"""

    db = DB(
        host=os.environ['DB_HOST'],
        db_name=os.environ['DB_NAME'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
    )
    bot = BotSettings(
        bot_token=os.environ['BOT_TOKEN'],
    )

    return Settings(
        db=db,
        bot=bot,
    )
