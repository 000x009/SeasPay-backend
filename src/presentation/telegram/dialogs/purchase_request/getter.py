import uuid
from typing import Dict, List

from aiogram_dialog import DialogManager

from dishka.integrations.aiogram import FromDishka

from src.application.dto.purchase_request import GetOnePurchaseRequestDTO
from src.application.services.purchase_request import PurchaseRequestService
from src.presentation.telegram.dialogs.common.injection import inject_getter
from src.infrastructure.json_text_getter import (
    get_purchase_request_text,
    get_purchase_request_price_text,
    get_purchase_product_loging_fields_text,
)
from src.infrastructure.config import load_settings


@inject_getter
async def purchase_request_text_getter(
    dialog_manager: DialogManager,
    purchase_request_service: FromDishka[PurchaseRequestService],
    **_,
) -> Dict[str, str]:
    request_id = dialog_manager.start_data.get('request_id')
    request = await purchase_request_service.get_request(GetOnePurchaseRequestDTO(id=uuid.UUID(request_id)))

    return {
        "request_text": get_purchase_request_text(
            user_id=request.user_id,
            request_id=request.id,
            purchase_url=request.purchase_url,
            created_at=request.created_at,
            status=request.status,
        ),
    }


@inject_getter
async def purchase_request_price_text_getter(
    dialog_manager: DialogManager,
    **_,
) -> Dict[str, str]:
    product_price = dialog_manager.dialog_data.get('price')
    if not product_price:
        price_text = ''
    else:
        settings = load_settings()
        final_price = float(product_price) + settings.commission.digital_product_usd_amount_commission
        price_text = get_purchase_request_price_text(final_price)

    return {
        "request_price_text": price_text,
    }


@inject_getter
async def purchase_product_loging_fields_text_getter(
    dialog_manager: DialogManager,
    **_,
) -> Dict[str, str]:
    login_fields = dialog_manager.dialog_data.get('login_fields')

    return {
        "login_fields": login_fields
    }


async def fields_getter(dialog_manager: DialogManager, **_) -> Dict[str, List[str]]:
    login_fields: list[str] = dialog_manager.dialog_data.get('login_fields')

    return {
        "fields": login_fields
    }
