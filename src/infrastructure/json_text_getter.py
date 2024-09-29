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
    created_at: datetime,
    status: OrderStatus,
    commission: int,
) -> str:
    status_text = {
        OrderStatus.NEW: "⌛ Ожидание обработки",
        OrderStatus.PROCESSING: "🔄 На обработке у администратора",
        OrderStatus.COMPLETE: "✅ Выполнен",
        OrderStatus.CANCEL: "❌ Отменен",
        OrderStatus.DELAY: "🕒 Отложен по техническим причинам",
    }

    return get_text_by_key("paypal_withdraw_order_text").format(
        id=order_id,
        user_id=user_id,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
        status=status_text[status],
        commission=commission,
    )


def get_order_commission_form_text(order_id: int) -> str:
    return get_text_by_key("admin_order_commission_form_text").format(order_id=order_id)


def get_user_must_receive_text(amount: float) -> str:
    return get_text_by_key("user_must_receive_text").format(amount=amount)


def get_withdraw_card_text(
    card_number: str,
    card_holder: str,
    user_must_receive: float,
    commission: float,
    profit: float,
) -> str:
    return get_text_by_key("withdraw_card_text").format(
        card_number=card_number,
        card_holder=card_holder,
        user_must_receive=user_must_receive,
        commission=commission,
        profit=profit,
    )


def get_withdraw_crypto_text(
    address: str,
    network: str,
    user_must_receive: float,
    commission: float,
    profit: float,
) -> str:
    return get_text_by_key("withdraw_crypto_text").format(
        address=address,
        network=network,
        user_must_receive=user_must_receive,
        commission=commission,
        profit=profit,
    )
