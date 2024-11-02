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
