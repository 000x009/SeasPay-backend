import json
from datetime import datetime
import os
from pathlib import Path
from decimal import Decimal
from typing import Optional
from uuid import UUID

from src.domain.value_objects.order import OrderStatusEnum, OrderTypeEnum
from src.domain.value_objects.purchase_request import RequestStatusEnum
from src.infrastructure.config import app_settings


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
        "NEW": "⌛ Ожидание обработки",
        "PROCESSING": "🔄 На обработке у администратора",
        "COMPLETE": "✅ Выполнен",
        "CANCEL": "❌ Отменен",
        "DELAY": "🕒 Отложен по техническим причинам",
        "NOT_PAID": "💳 Ожидает оплаты",
    }
    type_mapping = {
        OrderTypeEnum.WITHDRAW: "вывод средств",
        OrderTypeEnum.TRANSFER: "перевод средств",
        OrderTypeEnum.DIGITAL_PRODUCT: "приобретение виртуального продукта/услуги",
    }
    return get_text_by_key("paypal_order_text").format(
        type=type_mapping.get(order_type, ""),
        id=order_id,
        user_id=user_id,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
        status=status_mapping.get(status, ""),
    )


def get_digital_product_details_text(
    product_purchase_url: str,
    login_data: dict[str, str],
) -> str:
    login_fields = "\n".join([f"<b>• {key}</b>: <code>{value}</code>" for key, value in login_data.items()])

    return get_text_by_key("digital_product_details_text").format(
        purchase_url=product_purchase_url,
        generated_login_fields=login_fields,
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
    commission: Decimal,
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
    commission: Decimal,
    profit: float,
    asset: str,
    memo: Optional[str],
) -> str:
    return get_text_by_key("withdraw_crypto_text").format(
        address=address,
        network=network,
        user_must_receive=user_must_receive,
        commission=commission,
        profit=profit,
        asset=asset,
        memo=memo,
    )


def get_user_profile_text(
    user_id: int,
    total_withdrawn: Decimal,
    transfer_commission: Decimal,
    withdraw_commission: Decimal,
    product_purchase_commission: Decimal,
) -> str:
    return get_text_by_key("user_profile_text").format(
        user_id=user_id,
        total_withdrawn=total_withdrawn,
        transfer_commission=transfer_commission,
        withdraw_commission=withdraw_commission,
        product_purchase_commission=product_purchase_commission,
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
        "NEW": "⌛ Ожидание обработки",
        "PROCESSING": "🔄 На обработке у администратора",
        "COMPLETE": "✅ Выполнен",
        "CANCEL": "❌ Отменен",
        "DELAY": "🕒 Отложен по техническим причинам",
        "NOT_PAID": "💳 Ожидает оплаты",
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
    amount: Decimal,
    commission: Decimal,
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


def get_purchase_request_price_text(price: float) -> str:
    return get_text_by_key("purchase_request_price_text").format(price=price)


def get_purchase_product_loging_fields_text(login_fields: list[str]) -> str:
    return get_text_by_key("purchase_product_loging_fields_text").format(login_fields="\n".join(login_fields))


def get_cancel_purchase_reqeust_text(
    request_id: UUID,
    cancel_reason: str,
) -> str:
    return get_text_by_key("cancel_purchase_reqeust_text").format(
        request_id=request_id,
        cancel_reason=cancel_reason,
    )


def get_confirm_purchase_request_text(
    request_id: UUID,
) -> str:
    return get_text_by_key("confirm_purchase_request_text").format(
        request_id=request_id,
        application_fulfilling_url=app_settings.web.application_fulfilling_url.format(id=request_id),
    )


def get_platform_info_text(
    name: str,
    description: str,
    web_place: int,
    login_data: list[str],
) -> str:
    return get_text_by_key("platform_info_text").format(
        name=name,
        description=description,
        web_place=web_place,
        login_data="\n".join(map(lambda field: f"- <code>{field}</code>", login_data)),
    )


def get_platform_product_text(
    product_id: int,
    name: str,
    price: Decimal,
    instruction: str,
) -> str:
    return get_text_by_key("platform_product_text").format(
        product_id=product_id,
        name=name,
        price=price,
        instruction=instruction,
    )


def get_order_successfully_fulfilled_text(amount: float) -> str:
    return get_text_by_key("order_successfully_fulfilled_text").format(amount=amount)


def get_transfer_successfully_fulfilled_text(order_id: UUID) -> str:
    return get_text_by_key("transfer_successfully_fulfilled_text").format(order_id=order_id)


def get_digital_product_successfully_fulfilled_text(order_id: UUID) -> str:
    return get_text_by_key("digital_product_successfully_fulfilled_text").format(order_id=order_id)
