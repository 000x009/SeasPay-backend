from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from src.infrastructure.config import BotSettings
from src.presentation.telegram.buttons.callback_data import ConfirmOrderCallbackData


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


def get_order_kb_markup(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Выполнить', callback_data=ConfirmOrderCallbackData(order_id=order_id).pack()),
            ],
            [
                InlineKeyboardButton(text='❌ Отменить', callback_data=ConfirmOrderCallbackData(order_id=order_id).pack()),
            ],
            [
                InlineKeyboardButton(text='🛠️ Сообщить о проблеме', callback_data=ConfirmOrderCallbackData(order_id=order_id).pack()),
            ],
        ]
    )


def get_admin_order_confirmation_kb_markup(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Подтвердить', callback_data="..."),
            ],
        ]
    )
