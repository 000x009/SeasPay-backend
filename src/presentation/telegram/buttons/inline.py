from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from src.infrastructure.config import BotSettings
from src.presentation.telegram.buttons.callback_data.order import (
    OrderFulfillmentCallbackData,
    BackToOrderCallbackData,
    TakeOrderCallbackData,
)


def get_start_kb_markup(config: BotSettings) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🌊 Открыть OverseasPay', web_app=WebAppInfo(url=config.web_app_url)),
            ],
            [
                InlineKeyboardButton(text='📑 Условия пользования', url=config.terms_of_use_url),
                InlineKeyboardButton(text='💭 Техническая поддержка', url=config.technical_support_url),
            ]
        ]
    )


def get_order_fulfillment_kb_markup(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🔁 Начать выполнение', callback_data=OrderFulfillmentCallbackData(order_id=order_id).pack()),
            ],
        ]
    )



def get_admin_order_confirmation_kb_markup(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='◀️ Назад', callback_data=BackToOrderCallbackData(order_id=order_id).pack()),
            ],
        ]
    )


def get_take_order_kb_markup(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🗃️ Взяться за заказ', callback_data=TakeOrderCallbackData(order_id=order_id).pack()),
            ],
        ]
    )


def get_sent_money_kb_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='📨 Деньги отправлены пользователю', callback_data="money_sent"),
            ],
        ]
    )

