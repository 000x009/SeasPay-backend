from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from  fastapi_redis_cache import  cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.invoice import InvoiceService
from src.application.dto.invoice import GetInvoiceDTO, InvoiceDTO, UpdateInvoiceDTO
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.presentation.web_api.schema.invoice import UpdateInvoiceStatusSchema

router = APIRouter(
    tags=['Invoice'],
    prefix='/invoice',
    route_class=DishkaRoute,
)


@router.get('/{invoice_id}')
@cache(expire=60 * 60 * 24)
async def get_invoice(
    invoice_id: str,
    invoice_service: FromDishka[InvoiceService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> Optional[InvoiceDTO]:
    response = await invoice_service.get(GetInvoiceDTO(
        id=invoice_id,
        user_id=user_data.user.id,
    ))

    return response


@router.put('/')
@cache(expire=60 * 60 * 24)
async def update_invoice_status(
    data: UpdateInvoiceStatusSchema,
    invoice_service: FromDishka[InvoiceService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> JSONResponse:
    await invoice_service.update(UpdateInvoiceDTO(
        id=data.id,
        status=data.status,
    ))

    return JSONResponse(status_code=200, content={"message": "success"})
