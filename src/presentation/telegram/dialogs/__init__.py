from .order.dialog import order_dialog
from .admin.dialog import admin_dialog, look_up_order_dialog, admin_search_dialog

dialogs = [
    order_dialog,
    admin_dialog,
    look_up_order_dialog,
    admin_search_dialog,
]

__all__ = [
    'dialogs',
]
