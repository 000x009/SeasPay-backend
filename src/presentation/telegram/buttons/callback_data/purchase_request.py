from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class TakePurchaseRequestCallbackData(CallbackData, prefix='take_purchase_request'):
    request_id: UUID

