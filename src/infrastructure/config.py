import os
from pathlib import Path
from typing import Dict, Any
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
class Commission:
    """Commission settings"""

    min_withdraw_percentage: float
    max_withdraw_percentage: float
    min_withdraw_amount: float
    max_withdraw_amount: float
    max_transfer_amount: float
    max_transfer_percentage: float
    min_transfer_percentage: float
    digital_product_usd_amount_commission: float


@dataclass
class YandexCloudSettings:
    base_storage_url: str
    receipts_bucket_name: str
    feedbacks_bucket_name: str
    platforms_bucket_name: str
    access_key_id: str
    access_secret_key: str


@dataclass
class WebSettings:
    web_app_url: str
    application_fulfilling_url: str


@dataclass
class Settings:
    """App settings"""

    db: DB
    paypal: PayPal
    bot: BotSettings
    commission: Commission
    cloud_settings: YandexCloudSettings
    web: WebSettings


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
    web = WebSettings(
        web_app_url=os.environ['WEB_APP_URL'],
        application_fulfilling_url=os.environ['APPLICATION_FULFILLING_URL'],
    )

    config_path = Path(os.environ['TOML_CONFIG_PATH'])
    toml_cfg = load_toml_config(config_path)
    commission = Commission(
            min_withdraw_percentage=toml_cfg['commission']['paypal']['min-withdraw-percentage'],
            max_withdraw_percentage=toml_cfg['commission']['paypal']['max-withdraw-percentage'],
            min_withdraw_amount=toml_cfg['commission']['paypal']['min-withdraw-usd-amount'],
            max_withdraw_amount=toml_cfg['commission']['paypal']['max-withdraw-usd-amount'],
            max_transfer_amount=toml_cfg['commission']['paypal']['max-transfer-amount'],
            max_transfer_percentage=toml_cfg['commission']['paypal']['max-transfer-percentage'],
            min_transfer_percentage=toml_cfg['commission']['paypal']['min-transfer-percentage'],
            digital_product_usd_amount_commission=toml_cfg['commission']['digital-product']['usd-amount-commission'],
    )
    cloud_settings = YandexCloudSettings(
        access_key_id=toml_cfg['yandex-cloud']['yandex-access-key-id'],
        access_secret_key=toml_cfg['yandex-cloud']['yandex-access-secret-key'],
        platforms_bucket_name=toml_cfg['yandex-cloud']['platforms-bucket-name'],
        base_storage_url=toml_cfg['yandex-cloud']['base-storage-url'],
        receipts_bucket_name=toml_cfg['yandex-cloud']['receipts-bucket-name'],
        feedbacks_bucket_name=toml_cfg['yandex-cloud']['feedbacks-bucket-name'],
    )

    return Settings(
        db=db,
        paypal=paypal,
        bot=bot,
        commission=commission,
        cloud_settings=cloud_settings,
        web=web,
    )


def load_paypal_settings() -> PayPal:
    return load_settings().paypal


def load_bot_settings() -> BotSettings:
    return load_settings().bot


app_settings = load_settings()
