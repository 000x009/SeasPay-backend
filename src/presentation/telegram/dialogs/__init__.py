from .order.dialog import order_dialog
from .admin.dialog import admin_dialog, look_up_order_dialog, admin_search_dialog
from .purchase_request.dialog import purchase_request_fulfillment_dialog
from .platform.dialog import platform_dialog


dialogs = [
    order_dialog,
    admin_dialog,
    look_up_order_dialog,
    admin_search_dialog,
    purchase_request_fulfillment_dialog,
    platform_dialog,
]

__all__ = [
    'dialogs',
]
