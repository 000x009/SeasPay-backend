from src.presentation.telegram.handlers import start, admin_order

all_handlers = [
    start.router,
    admin_order.router,
]

__all__ = ['handlers']
