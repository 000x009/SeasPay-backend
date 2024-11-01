from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Multi, Const
from aiogram_dialog.widgets.kbd import SwitchTo

from src.presentation.telegram.states.purchase_request import PurchaseRequestFulfillmentSG


purchase_request_fulfillment_dialog = Dialog(
  Window(
    Multi(
        Format("{request_text}\n"),
        Format("{request_price_text}\n"),
        Format("{request_login_fields_text}\n"),
    ),
    SwitchTo(
        id="set_price_button",
        text=Const("Установить цену продукта"),
        state=PurchaseRequestFulfillmentSG.ADD_PRICE,
    ),
    SwitchTo(
        id="set_login_fields_button",
        text=Const("Установить поля для логина"),
        state=PurchaseRequestFulfillmentSG.ADD_LOGIN_FIELDS,
    ),
    SwitchTo(
        id="confirm_button",
        text=Const("✅ Подтвердить запрос"),
        state=PurchaseRequestFulfillmentSG.PRE_CONFIRM_FULFILLMENT,
    ),
    SwitchTo(
        id="cancel_button",
        text=Const("❌ Отменить запрос"),
        state=PurchaseRequestFulfillmentSG.CANCEL_REASON,
    ),
    state=PurchaseRequestFulfillmentSG.REQUEST_INFO,
  )
)
