import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class BaseDB:
    """Base database config"""

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
    """Telegram bot settings"""

    bot_token: str
    orders_group_id: str
    webhook_url: str


@dataclass
class PayPal:
    """PayPal settings"""

    client_id: str
    client_secret: str
    api_base_url: str


@dataclass
class Settings:
    """App settings"""

    db: DB
    paypal: PayPal
    bot: BotSettings


def load_settings() -> Settings:
    """Get app settings"""
    load_dotenv(override=True)

    db = DB(
        host=os.environ['DB_HOST'],
        db_name=os.environ['DB_NAME'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
    )
    paypal = PayPal(
        client_id=os.environ['PAYPAL_CLIENT_ID'],
        client_secret=os.environ['PAYPAL_CLIENT_SECRET'],
        api_base_url=os.environ['PAYPAL_BASE_URL'],
    )
    bot = BotSettings(
        bot_token=os.environ['BOT_TOKEN'],
        orders_group_id=os.environ['ORDERS_GROUP_ID'],
        webhook_url=os.environ['WEBHOOK_URL'],
    )

    return Settings(
        db=db,
        paypal=paypal,
        bot=bot,
    )


def load_paypal_settings() -> PayPal:
    return load_settings().paypal


def load_bot_settings() -> BotSettings:
    return load_settings().bot
