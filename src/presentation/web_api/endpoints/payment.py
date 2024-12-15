from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from aiogram.utils.web_app import WebAppInitData

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.services.payment import PaymentService
from src.application.services.cryptopay import CryptopayService
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.application.dto.payment import (
    CreatePaymentDTO,
    PaymentDTO,
    GetPaymentDTO,
    ReceivePaymentDTO,
)
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


@router.get('/crypto-pay/exchange-rates')
async def get_exchange_rates(
    cryptopay_service: FromDishka[CryptopayService],
) -> None:
    await cryptopay_service.get_exchange_rates()


@router.get('/', response_model=PaymentDTO)
async def get_payment(
    id: UUID,
    payment_service: FromDishka[PaymentService],
) -> PaymentDTO:
    response = await payment_service.get(GetPaymentDTO(payment_id=id))

    return response


@router.post('/receive-payment')
async def receive_payment(
    request: Request,
    payment_service: FromDishka[PaymentService],
) -> JSONResponse:
    request_data = await request.json()
    print(request_data)
    if request_data.get('update_type') == 'invoice_paid':
        invoice = request_data.get('payload')
        payment_id = UUID(invoice.get('payload'))
        await payment_service.receive_payment(ReceivePaymentDTO(payment_id=payment_id))

    return JSONResponse(status_code=200, content={"message": "success"})
