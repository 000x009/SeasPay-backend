from aiogram import F

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Multi, Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Row,
    ScrollingGroup,
    Select,
    PrevPage,
    CurrentPage,
    NextPage,
    SwitchTo,
    Button,
)

from src.presentation.telegram.states.purchase_request import PurchaseRequestFulfillmentSG
from src.presentation.telegram.dialogs.purchase_request.getter import (
    purchase_request_text_getter,
    purchase_request_price_text_getter,
    purchase_product_loging_fields_text_getter,
    fields_getter,
)
from src.presentation.telegram.dialogs.purchase_request.handlers import (
    on_field_name,
    remove_field,
    confirm_purchase_request,
    on_reason_cancel_purchase_request,
    on_input_price,
)


purchase_request_fulfillment_dialog = Dialog(
    Window(
        Multi(
            Format("{request_text}\n"),
            Format("{request_price_text}\n"),
        ),
        SwitchTo(
            id="set_price_button",
            text=Const("🈂️ Установить цену продукта"),
            state=PurchaseRequestFulfillmentSG.ADD_PRICE,
        ),
        SwitchTo(
            id="set_login_fields_button",
            text=Const("📝 Поля для логина"),
            state=PurchaseRequestFulfillmentSG.LOGIN_FIELDS,
        ),
        SwitchTo(
            id="confirm_button",
            text=Const("✅ Одобрить запрос"),
            state=PurchaseRequestFulfillmentSG.PRE_CONFIRM_FULFILLMENT,
            when=F['login_fields'] & F['request_price_text'],
        ),
        SwitchTo(
            id="cancel_button",
            text=Const("❌ Отменить запрос"),
            state=PurchaseRequestFulfillmentSG.CANCEL_REASON,
        ),
        getter=[  # type: ignore
            purchase_request_text_getter,
            purchase_request_price_text_getter,
            purchase_product_loging_fields_text_getter,
        ],
        state=PurchaseRequestFulfillmentSG.REQUEST_INFO,
    ),
    Window(
        Format("Введите цену продукта в USD:"),
        MessageInput(
            func=on_input_price,
        ),
        SwitchTo(
            id="set_price_button",
            text=Const("◀️ Назад"),
            state=PurchaseRequestFulfillmentSG.REQUEST_INFO,
        ),
        state=PurchaseRequestFulfillmentSG.ADD_PRICE,
    ),
    Window(
        Format("Поля для логина:", when=F['login_fields']),
        Format("Поля для логина отсутствуют", when=~F['login_fields']),
        ScrollingGroup(
            Select(
                id="field_select",
                items="fields",
                item_id_getter=lambda item: item,
                text=Format("{item}"),
                on_click=remove_field,
                when="fields",
            ),
            id="field_group",
            height=10,
            width=1,
            hide_on_single_page=True,
            hide_pager=True,
            when="fields"
        ),
        Row(
            PrevPage(
                scroll="order_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="order_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="order_group", text=Format("▶️"),
            ),
            when=F['fields'].len() > 10,
        ),
        SwitchTo(
            text=Const("🔗 Добавить поле"),
            id="add_login_field",
            state=PurchaseRequestFulfillmentSG.ADD_LOGIN_FIELD,
        ),
        SwitchTo(
            id="set_login_fields_button",
            text=Const("◀️ Назад"),
            state=PurchaseRequestFulfillmentSG.REQUEST_INFO,
        ),
        getter=fields_getter,
        state=PurchaseRequestFulfillmentSG.LOGIN_FIELDS,
    ),
    Window(
        Const("Введите название поля:"),
        MessageInput(
            func=on_field_name,
        ),
        state=PurchaseRequestFulfillmentSG.ADD_LOGIN_FIELD,
    ),
    Window(
        Format("Вы уверены, что хотите одобрить запрос на покупку виртуального товара/услуги?"),
        Button(
            text=Const("✅ Да"),
            id="confirm_fulfillment",
            on_click=confirm_purchase_request,
        ),
        SwitchTo(
            id="confirm_button",
            text=Const("◀️ Назад"),
            state=PurchaseRequestFulfillmentSG.REQUEST_INFO,
        ),
        state=PurchaseRequestFulfillmentSG.PRE_CONFIRM_FULFILLMENT,
    ),
    Window(
        Format("Напишите причину отмены запроса для пользователя:"),
        MessageInput(
            func=on_reason_cancel_purchase_request,
        ),
        SwitchTo(
            id="cancel_button",
            text=Const("◀️ Назад"),
            state=PurchaseRequestFulfillmentSG.REQUEST_INFO,
        ),
        state=PurchaseRequestFulfillmentSG.CANCEL_REASON,
    ),
)
