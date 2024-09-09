from src.presentation.telegram.handlers import start

all_handlers = [
    start.router,
]

__all__ = ['handlers']
