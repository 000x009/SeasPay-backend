from typing import Dict

from aiogram_dialog.widgets.common.when import Predicate, Whenable
from aiogram_dialog import DialogManager


def new_no_user() -> Predicate:
    def when_no_user(
        data: Dict,
        widget: Whenable,
        manager: DialogManager,
    ) -> bool:
        payment_receipt = manager.dialog_data.get("payment_receipt_id")
        received_amount = manager.dialog_data.get("received_amount")
        user_must_receive = manager.dialog_data.get("user_must_receive")
        user_received_amount = manager.dialog_data.get("user_received_amount")

        if payment_receipt and received_amount and user_must_receive and user_received_amount:
            return True
        return False

    return when_confirm_fulfillment
