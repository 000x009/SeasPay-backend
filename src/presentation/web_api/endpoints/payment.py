from fastapi import APIRouter, Depends

from aiogram.utils.web_app import WebAppInitData

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.services.payment import PaymentService
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.application.dto.payment import CreatePaymentDTO, PaymentDTO
from src.presentation.web_api.schema.payment import CreateCryptoPayInvoiceSchema

router = APIRouter(
    prefix='/payment',
    tags=['Payment'],
    route_class=DishkaRoute,
)


@router.post('/crypto-pay/create-invoice', response_model=PaymentDTO)
async def create_crypto_pay_invoice(
    data: CreateCryptoPayInvoiceSchema,
    payment_service: FromDishka[PaymentService],
    user_init_data: WebAppInitData = Depends(user_init_data_provider),
) -> PaymentDTO:
    response = await payment_service.create(
        CreatePaymentDTO(
            user_id=user_init_data.user.id,
            amount=data.amount,
        )
    )

    return response
