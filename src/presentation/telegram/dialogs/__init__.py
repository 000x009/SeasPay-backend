from .order.dialog import order_dialog
from .admin.dialog import admin_dialog

dialogs = [
    order_dialog,
    admin_dialog,
]

__all__ = [
    'dialogs',
]
