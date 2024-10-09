from typing import Dict

from aiogram_dialog.widgets.common.when import Predicate, Whenable
from aiogram_dialog import DialogManager


def new_confirm_fulfillment() -> Predicate:
    def when_confirm_fulfillment(
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


def new_when_no_payment_receipt() -> Predicate:
    def when_no_payment_receipt(
        data: Dict,
        widget: Whenable,
        manager: DialogManager,
    ) -> bool:
        return manager.dialog_data.get("payment_receipt_id") is None

    return when_no_payment_receipt
