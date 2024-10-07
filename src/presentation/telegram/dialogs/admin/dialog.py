from aiogram import F

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Row,
    ScrollingGroup,
    Select,
    PrevPage,
    CurrentPage,
    NextPage,
    Back,
)
from aiogram_dialog.widgets.text import Format, Const

from src.presentation.telegram.dialogs.admin.getter import order_getter, one_order_getter
from src.presentation.telegram.states import AdminUserOrdersSG
from src.presentation.telegram.dialogs.admin.handlers import selected_order


admin_dialog = Dialog(
    Window(
        Const("Заказы пользователя", when="orders"),
        ScrollingGroup(
            Select(
                id="order_select",
                items="orders",
                item_id_getter=lambda item: item.id,
                text=Format("№{item.id}"),
                on_click=selected_order,
                when="orders",
            ),
            id="order_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True
        ),
        Row(
            PrevPage(
                scroll="order_group", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="order_group", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="order_group", text=Format("▶️"),
            ),
            when="orders",
        ),
        state=AdminUserOrdersSG.USER_ORDERS,
        getter=order_getter,
    ),
    Window(
        Format("{order_text}"),
        Back(
            text=Format("◀️ Назад"),
        ),
        state=AdminUserOrdersSG.ONE_ORDER,
        getter=one_order_getter,
    )
)