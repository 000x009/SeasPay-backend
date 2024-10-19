import json
from datetime import datetime
import os
from pathlib import Path
from decimal import Decimal
from uuid import UUID
from src.domain.value_objects.order import OrderStatusEnum, OrderTypeEnum
from src.domain.value_objects.purchase_request import RequestStatusEnum

def get_text_by_key(key: str) -> str:
    with open(os.path.normpath(Path("files/json/texts.json")), encoding="utf-8") as f:
        data = json.load(f)

        return data[key]


def get_paypal_order_text(
    order_id: UUID,
    user_id: int,
    created_at: datetime,
    status: OrderStatusEnum,
    order_type: OrderTypeEnum,
) -> str:
    status_mapping = {
        OrderStatusEnum.NEW: "⌛ Ожидание обработки",
        OrderStatusEnum.PROCESSING: "🔄 На обработке у администратора",
        OrderStatusEnum.COMPLETE: "✅ Выполнен",
        OrderStatusEnum.CANCEL: "❌ Отменен",
        OrderStatusEnum.DELAY: "🕒 Отложен по техническим причинам",
    }
    type_mapping = {
        OrderTypeEnum.WITHDRAW: "вывод средств",
        OrderTypeEnum.TRANSFER: "перевод средств",
        OrderTypeEnum.DIGITAL_PRODUCT: "приобретение продукта",
    }
    return get_text_by_key("paypal_order_text").format(
        type=type_mapping.get(order_type, ""),
        id=order_id,
        user_id=user_id,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
        status=status_mapping.get(status, ""),
    )


def get_paypal_withdraw_order_preview_text(
    order_id: UUID,
    user_id: int,
    created_at: datetime,
    commission: int,
) -> str:
    return get_text_by_key("paypal_withdraw_order_preview_text").format(
        id=order_id,
        user_id=user_id,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
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


def get_user_profile_text(
    user_id: int,
    commission: int,
    total_withdrawn: Decimal,
) -> str:
    return get_text_by_key("user_profile_text").format(
        user_id=user_id,
        commission=commission,
        total_withdrawn=total_withdrawn,
    )


def get_order_info_card_text(
    order_id: UUID,
    user_id: int,
    commission: float,
    created_at: datetime,
    status: OrderStatusEnum,
    card_number: str,
    card_holder: str,
) -> str:
    return get_text_by_key("order_info_card_text").format(
        id=order_id,
        user_id=user_id,
        commission=commission,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
        status=status.value,
        card_number=card_number,
        card_holder=card_holder,
    )


def get_order_info_crypto_text(
    order_id: UUID,
    user_id: int,
    commission: float,
    created_at: datetime,
    status: OrderStatusEnum,
    address: str,
    network: str,
) -> str:
    status_text = {
        OrderStatusEnum.NEW: "⌛ Ожидание обработки",
        OrderStatusEnum.PROCESSING: "🔄 На обработке у администратора",
        OrderStatusEnum.COMPLETE: "✅ Выполнен",
        OrderStatusEnum.CANCEL: "❌ Отменен",
        OrderStatusEnum.DELAY: "🕒 Отложен по техническим причинам",
    }
    return get_text_by_key("order_info_crypto_text").format(
        id=order_id,
        user_id=user_id,
        commission=commission,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
        status=status_text.get(status, ""),
        address=address,
        network=network,
    )


def get_admin_service_statistics_text(
    all_time_profit: Decimal,
    month_profit: Decimal,
    week_profit: Decimal,
    all_users_amount: int,
    new_month_users: int,
    new_week_users: int,
    new_day_users: int,
    total_withdrawn: Decimal,
) -> str:
    return get_text_by_key("admin_service_statistics_text").format(
        all_time_profit=all_time_profit,
        month_profit=month_profit,
        week_profit=week_profit,
        all_users_amount=all_users_amount,
        new_month_users=new_month_users,
        new_week_users=new_week_users,
        new_day_users=new_day_users,
        total_withdrawn=total_withdrawn,
    )


def get_transfer_text(
    receiver_email: str,
    amount: float,
    commission: float,
) -> str:
    return get_text_by_key("transfer_text").format(
        receiver_email=receiver_email,
        amount=amount,
        commission=commission,
    )


def get_purchase_request_text(
    request_id: UUID,
    user_id: int,
    purchase_url: str,
    created_at: datetime,
    status: RequestStatusEnum,
) -> str:
    status_mapping = {
        RequestStatusEnum.PENDING: "⌛ Ожидание обработки",
        RequestStatusEnum.CONFIRMED: "✅ Обработан",
        RequestStatusEnum.CANCELLED: "❌ Отменен",
    }
    return get_text_by_key("purchase_request_text").format(
        id=request_id,
        user_id=user_id,
        purchase_url=purchase_url,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
        status=status_mapping.get(status, ""),
    )
