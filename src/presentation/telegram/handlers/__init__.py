from src.presentation.telegram.handlers import admin, start

all_handlers = [
    start.router,
    admin.router,
]

__all__ = ['handlers']
