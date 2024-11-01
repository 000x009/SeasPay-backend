import uuid
import logging

from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from dishka.integrations.aiogram import FromDishka

from src.presentation.telegram.states.purchase_request import PurchaseRequestFulfillmentSG
from src.application.services.purchase_request import PurchaseRequestService
from src.presentation.telegram.dialogs.common.injection import inject_on_click
from src.application.dto.purchase_request import CancelPurchaseRequestDTO
from src.infrastructure.json_text_getter import get_cancel_purchase_reqeust_text, get_confirm_purchase_request_text
from src.application.dto.purchase_request import ConfirmPurchaseRequestDTO
from src.presentation.telegram.buttons import inline
from src.application.services.product_application import ProductApplicationService
from src.application.dto.product_application import GetProductApplicationByRequestIdDTO


async def on_field_name(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
) -> None:
    login_fields = dialog_manager.dialog_data.get('login_fields', [])
    login_fields.append(message.text.strip())
    dialog_manager.dialog_data['login_fields'] = login_fields
    await dialog_manager.switch_to(PurchaseRequestFulfillmentSG.LOGIN_FIELDS)


async def remove_field(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    field: str,
) -> None:
    login_fields = dialog_manager.dialog_data.get('login_fields', [])
    login_fields.remove(field)
    dialog_manager.dialog_data['login_fields'] = login_fields
    await dialog_manager.switch_to(PurchaseRequestFulfillmentSG.LOGIN_FIELDS)


async def on_input_price(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
) -> None:
    if message.text.isdigit():
        dialog_manager.dialog_data['price'] = float(message.text)
        await dialog_manager.switch_to(PurchaseRequestFulfillmentSG.REQUEST_INFO)
    else:
        bot: Bot = dialog_manager.middleware_data.get('bot')
        await bot.send_message(
            chat_id=message.chat.id,
            text='Цена должна быть числом!',
        )


@inject_on_click
async def on_reason_cancel_purchase_request(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    purchase_request_service: FromDishka[PurchaseRequestService],
) -> None:
    request_id = dialog_manager.start_data.get('request_id')
    request = await purchase_request_service.cancel_request(CancelPurchaseRequestDTO(
        request_id=uuid.UUID(request_id),
    ))
    bot: Bot = dialog_manager.middleware_data.get('bot')
    await bot.send_message(
        chat_id=message.chat.id,
        text=get_cancel_purchase_reqeust_text(
            request_id=request.id,
            cancel_reason=message.text,
        ),
    )
    await dialog_manager.done()


@inject_on_click
async def confirm_purchase_request(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    purchase_request_service: FromDishka[PurchaseRequestService],
    application_service: FromDishka[ProductApplicationService],
) -> None:
    request_id = dialog_manager.start_data.get('request_id')
    login_fields = dialog_manager.dialog_data.get('login_fields')
    price = dialog_manager.dialog_data.get('price')

    try:
        request = await purchase_request_service.confirm_request(ConfirmPurchaseRequestDTO(
            request_id=uuid.UUID(request_id),
            login_fields=login_fields,
            price=price,
        ))
        application = await application_service.get_application_by_request_id(GetProductApplicationByRequestIdDTO(
            purchase_request_id=request.id,
        ))
        bot: Bot = dialog_manager.middleware_data.get('bot')
        await bot.send_message(
            chat_id=request.user_id,
            text=get_confirm_purchase_request_text(request_id=application.id),
            reply_markup=inline.fulfill_product_application_kb_markup(application.id),
        )
    except Exception as e:
        logging.error(e)
    finally:
        await dialog_manager.done()
