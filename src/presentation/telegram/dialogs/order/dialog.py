from aiogram import F

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const, Multi
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format, Const

from src.presentation.telegram.dialogs.order.getter import order_getter, order_cancel_getter, order_text_getter
from src.domain.value_objects.order import OrderTypeEnum
from src.presentation.telegram.states import OrderFulfillmentSG
from src.presentation.telegram.dialogs.order.handlers import (
    on_wrote_paypal_received_amount,
    calculate_commission,
    attach_receipt,
    on_attach_receipt,
    pre_confirm_fulfillment,
    confirm_fulfillment,
    cancel_order_handler,
    on_reason_cancel_order,
    on_user_received_amount
)
from src.presentation.telegram.dialogs.order.predicate import new_confirm_fulfillment, new_when_no_payment_receipt


order_dialog = Dialog(
    Window(
        DynamicMedia("payment_receipt", when="payment_receipt"),
        Multi(
            Format("{order_text}\n"),
            Format("{details_text}"),
        ),
        Button(
            text=Const("🧮 Рассчитать комиссию"),
            id="calculate_commission",
            on_click=calculate_commission,
            when=F['order'].type == OrderTypeEnum.WITHDRAW,
        ),
        SwitchTo(
            text=Const("🪙 Полученная сумма пользователем"),
            id="user_received_amount",
            state=OrderFulfillmentSG.USER_RECEIVED_AMOUNT,
            when=F['order'].type == OrderTypeEnum.WITHDRAW,
        ),
        Button(
            text=Const("🖇️ Прикрепить фото чека"),
            id="attach_receipt",
            on_click=attach_receipt,
            when=new_when_no_payment_receipt(),
        ),
        Button(
            text=Const("🖇️ Поменять фото чека"),
            id="attach_receipt",
            on_click=attach_receipt,
            when="payment_receipt",
        ),
        Button(
            text=Const("✅ Подтвердить выполнение"),
            id="pre_confirm_fulfillment",
            on_click=pre_confirm_fulfillment,
            when=new_confirm_fulfillment(),
        ),
        SwitchTo(
            text=Const("❌ Отменить заказ"),
            id='cancel_order',
            state=OrderFulfillmentSG.PRE_CONFIRM_CANCEL,
        ),
        getter=[order_getter, order_text_getter],
        state=OrderFulfillmentSG.ORDER_INFO,
    ),
    Window(
        Const('🖊️ Напишите полученную сумму на PayPal (USD):'),
        TextInput(
            id='write_answer',
            on_success=on_wrote_paypal_received_amount,
        ),
        Back(Format('◀️ Назад')),
        state=OrderFulfillmentSG.CALCULATE_COMMISSION,
    ),
    Window(
        Const('Отправьте фото чека, полученной суммы'),
        MessageInput(
            func=on_attach_receipt,
            content_types=["photo"],
        ),
        SwitchTo(
            id='back_to_order_info',
            text=Const('◀️ Назад'),
            state=OrderFulfillmentSG.ORDER_INFO,
        ),
        state=OrderFulfillmentSG.ATTACH_RECEIPT,
    ),
    Window(
        Const('Вы уверены что хотите подтвердить выполнение заказа?'),
        Button(
            text=Const('✅ Да'),
            id="confirm_fulfillment",
            on_click=confirm_fulfillment,
        ),
        SwitchTo(
            id='back_to_order_info_',
            text=Const('◀️ Назад'),
            state=OrderFulfillmentSG.ORDER_INFO,
        ),
        state=OrderFulfillmentSG.PRE_CONFIRM,
    ),
    Window(
        Const('Напишите причину отмены заказа:'),
        MessageInput(
            func=on_reason_cancel_order,
        ),
        SwitchTo(
            id='back_to_order_info_',
            text=Const('◀️ Назад'),
            state=OrderFulfillmentSG.ORDER_INFO,
        ),
        state=OrderFulfillmentSG.PRE_CONFIRM_CANCEL,
    ),
    Window(
        Format('Вы уверены что хотите отменить данный заказ с данной причиной?\n\n <blockquote>{reason}</blockquote>'),
        Button(
            text=Const('✅ Да'),
            id="confirm_fulfillment",
            on_click=cancel_order_handler,
        ),
        SwitchTo(
            id='back_to_pre_confirm_cancel',
            text=Const('◀️ Назад'),
            state=OrderFulfillmentSG.PRE_CONFIRM_CANCEL,
        ),
        getter=order_cancel_getter,
        state=OrderFulfillmentSG.CANCEL_ORDER,
    ),
    Window(
        Const('Если вы сделали все операции и пользователь получил свои деньги, то отправьте данную сумму в USD:'),
        MessageInput(
            func=on_user_received_amount,
        ),
        SwitchTo(
            id='back_to_order_info_',
            text=Const('◀️ Назад'),
            state=OrderFulfillmentSG.ORDER_INFO,
        ),
        state=OrderFulfillmentSG.USER_RECEIVED_AMOUNT,
    )
)
