import os
from pathlib import Path
from typing import Dict, Any, Union
from dataclasses import dataclass

import toml
from dotenv import load_dotenv


def load_toml_config(path: Path) -> Dict[str, Any]:
    with open(os.path.normpath(path), 'r') as file:
        return toml.load(file)


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
    orders_group_id: int
    webhook_url: str
    terms_of_use_url: str
    web_app_url: str
    technical_support_url: str


@dataclass
class PayPal:
    """PayPal settings"""

    client_id: str
    client_secret: str
    api_base_url: str


@dataclass
class AmazonConfig:
    """Amazon S3 cloud storage config"""

    bucket: str
    access_key: str
    secret_key: str


@dataclass
class PayPalCommission:
    """PayPal commission settings"""

    min_percentage_to_withdraw: int
    max_percentage_to_withdraw: int
    min_amount_to_withdraw: Union[float, str]
    max_amount_to_withdraw: Union[float, str]
    max_amount_to_transfer: Union[float, str]
    commission_to_transfer: float


@dataclass
class Commission:
    """Commission settings"""

    paypal: PayPalCommission


@dataclass
class Settings:
    """App settings"""

    db: DB
    paypal: PayPal
    bot: BotSettings
    commission: Commission


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
        orders_group_id=int(os.environ['ORDERS_GROUP_ID']),
        webhook_url=os.environ['WEBHOOK_URL'],
        terms_of_use_url=os.environ['TELEGRAPH_TERMS_OF_USE_URL'],
        web_app_url=os.environ['WEB_APP_URL'],
        technical_support_url=os.environ['TECHNICAL_SUPPORT_URL'],
    )

    config_path = Path(os.environ['TOML_CONFIG_PATH'])
    toml_cfg = load_toml_config(config_path)
    commission = Commission(
        paypal=PayPalCommission(
            min_percentage_to_withdraw=toml_cfg['commission']['paypal']['min_percentage_to_withdraw'],
            max_percentage_to_withdraw=toml_cfg['commission']['paypal']['max_percentage_to_withdraw'],
            min_amount_to_withdraw=toml_cfg['commission']['paypal']['min_amount_to_withdraw'],
            max_amount_to_withdraw=toml_cfg['commission']['paypal']['max_amount_to_withdraw'],
            max_amount_to_transfer=toml_cfg['commission']['paypal']['max_amount_to_transfer'],
            commission_to_transfer=toml_cfg['commission']['paypal']['commission_to_transfer'],
        )
    )

    return Settings(
        db=db,
        paypal=paypal,
        bot=bot,
        commission=commission,
    )


def load_paypal_settings() -> PayPal:
    return load_settings().paypal


def load_bot_settings() -> BotSettings:
    return load_settings().bot
