import json
from datetime import datetime
import os
from pathlib import Path

from src.domain.value_objects.order import OrderStatus


def get_text_by_key(key: str) -> str:
    with open(os.path.normpath(Path("src/files/json/texts.json")), encoding="utf-8") as f:
        data = json.load(f)

        return data[key]


def get_paypal_withdraw_order_text(
    order_id: int,
    user_id: int,
    username: str,
    created_at: datetime,
    status: OrderStatus,
    commission: int,
) -> str:
    status_text = {
        OrderStatus.WAIT: "⌛ Ожидание",
        OrderStatus.COMPLETE: "✅ Выполнен",
        OrderStatus.CANCEL: "❌ Отменен",
        OrderStatus.DELAY: "🕒 Отложен",
    }

    return get_text_by_key("paypal_withdraw_order_text").format(
        id=order_id,
        user_id=user_id,
        username=username,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
        status=status_text[status],
        commission=commission,
    )
