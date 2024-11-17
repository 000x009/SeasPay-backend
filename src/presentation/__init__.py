import logging

from fastapi import FastAPI

from src.presentation.web_api.endpoints import (
    user,
    feedback,
    order,
    cloud,
    purchase_request,
    product_application,
    platform,
    platform_product,
)
from src.presentation.web_api.exception_handlers import (
    user as user_exception,
    user_commission as user_commission_exception,
    user_topic as user_topic_exception,
    transfer_details as transfer_details_exception,
    withdraw_details as withdraw_details_exception,
    platform as platform_exception,
    platform_product as platform_product_exception,
    purchase_request as purchase_request_exception,
    completed_order as completed_order_exception,
    order as order_exception,

)
from src.domain.exceptions.user import UserDataError, UserNotFoundError, NotAuthorizedError
from src.domain.exceptions.order import OrderNotFoundError, OrderAlreadyTakenError
from src.domain.exceptions.user_commission import UserCommissionNotFoundError, UserCommissionDataError
from src.domain.exceptions.user_topic import TopicNotFoundError
from src.domain.exceptions.transfer_details import TransferDetailsNotFound, TransferDetailsDataError
from src.domain.exceptions.withdraw_details import WithdrawDetailsNotFound, WithdrawDetailsDataError
from src.domain.exceptions.platform import PlatformDataError
from src.domain.exceptions.platform_product import PlatformProductDataError
from src.domain.exceptions.purchase_request import PurchaseRequestAlreadyTaken, PurchaseRequestNotFound
from src.domain.exceptions.completed_order import CompletedOrderNotFoundError, CompletedOrderDataError


def include_all_routers(app: FastAPI) -> None:
    app.include_router(user.router)
    app.include_router(feedback.router)
    app.include_router(order.router)
    app.include_router(cloud.router)
    app.include_router(purchase_request.router)
    app.include_router(product_application.router)
    app.include_router(platform.router)
    app.include_router(platform_product.router)
    
    logging.info('All API routers was included.')


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        NotAuthorizedError, user_exception.not_authorized_exception_handler,
    )
    app.add_exception_handler(
        UserNotFoundError, user_exception.user_not_found_exception_handler,
    )
    app.add_exception_handler(
        UserDataError, user_exception.user_data_exception_handler,
    )

    app.add_exception_handler(
        OrderAlreadyTakenError, order_exception.order_already_taken_exception_handler,
    )
    app.add_exception_handler(
        OrderNotFoundError, order_exception.order_not_found_exception_handler,
    )

    app.add_exception_handler(
        UserCommissionNotFoundError, user_commission_exception.commission_not_found_handler,
    )
    app.add_exception_handler(
        UserCommissionDataError, user_commission_exception.commission_data_error,
    )

    app.add_exception_handler(
        TopicNotFoundError, user_topic_exception.topic_not_found_handler,
    )

    app.add_exception_handler(
        TransferDetailsNotFound, transfer_details_exception.transfer_not_found_handler,
    )
    app.add_exception_handler(
        TransferDetailsDataError, transfer_details_exception.transfer_data_handler,
    )

    app.add_exception_handler(
        WithdrawDetailsNotFound, withdraw_details_exception.withdraw_details_not_found_handler,
    )
    app.add_exception_handler(
        WithdrawDetailsDataError, withdraw_details_exception.withdraw_details_data_error_handler,
    )

    app.add_exception_handler(
        PlatformDataError, platform_exception.platform_data_exception_handler,
    )

    app.add_exception_handler(
        PlatformProductDataError, platform_product_exception.platform_product_data_exception_handler,
    )

    app.add_exception_handler(
        PurchaseRequestAlreadyTaken, purchase_request_exception.request_already_taken_handler,
    )
    app.add_exception_handler(
        PurchaseRequestNotFound, purchase_request_exception.request_not_found_handler,
    )

    app.add_exception_handler(
        CompletedOrderNotFoundError, completed_order_exception.completed_order_not_found_exception_handler,
    )
    app.add_exception_handler(
        CompletedOrderDataError, completed_order_exception.completed_order_data_exception_handler,
    )
