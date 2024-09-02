import json
from datetime import datetime
import os
from pathlib import Path
from decimal import Decimal

from src.domain.value_objects.order import OrderStatus


def get_text_by_key(key: str) -> str:
    with open(os.path.normpath(Path("src/files/json/texts.json")), encoding="utf-8") as f:
        data = json.load(f)

        return data[key]


def get_paypal_withdraw_order_text(
    order_id: int,
    user_id: int,
    username: str,
    amount: Decimal,
    created_at: datetime,
    status: OrderStatus,
) -> str:
    return get_text_by_key("paypal_withdraw_order_text").format(
        id=order_id,
        user_id=user_id,
        username=username,
        amount=amount,
        created_at=created_at,
        status=status,
    )
