import logging

from fastapi import FastAPI

from src.presentation.endpoints import user, feedback, order


def include_all_routers(app: FastAPI) -> None:
    app.include_router(user.router)
    app.include_router(feedback.router)
    app.include_router(order.router)

    logging.info('All API routers was included.')
