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
    SwitchTo,
    Button,
)
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.presentation.telegram.dialogs.admin.getter import (
    order_getter,
    one_order_getter,
    all_orders_getter,
    processing_orders_getter,
    completed_orders_getter,
    cancelled_orders_getter,
)
from src.presentation.telegram.dialogs.common.handler import message_input_fixing
from src.presentation.telegram.states import AdminUserOrdersSG, AdminOrderLookUpSG
from src.presentation.telegram.dialogs.admin.handlers import selected_order, selected_order_look_up, switch_to_fulfillment


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
        MessageInput(
            func=message_input_fixing,
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


look_up_order_dialog = Dialog(
    Window(
        Const('Выберите по кнопкам ниже какие заказы вы хотите просмотреть:'),
        SwitchTo(
            text=Const('🌐 Все заказы'),
            id='all_orders',
            state=AdminOrderLookUpSG.ALL_ORDERS,
        ),
        SwitchTo(
            text=Const('🔄 Не выполненные заказы'),
            id='processing_orders',
            state=AdminOrderLookUpSG.PROCESSING_ORDERS,
        ),
        SwitchTo(
            text=Const('✅ Выполненные заказы'),
            id='completed_orders',
            state=AdminOrderLookUpSG.COMPLETED_ORDERS,
        ),
        SwitchTo(
            text=Const('❌ Отмененные заказы'),
            id='cancelled_orders',
            state=AdminOrderLookUpSG.CANCELLED_ORDERS,
        ),
        MessageInput(
            func=message_input_fixing,
        ),
        state=AdminOrderLookUpSG.START,
    ),
    Window(
        Format('🌐 Все заказы ({count})', when="orders"),
        Format("На данный момент еще нет заказов", when="is_empty"),
        ScrollingGroup(
            Select(
                id="order_select",
                items="orders",
                item_id_getter=lambda item: item.id,
                text=Format("№{item.id}"),
                on_click=selected_order_look_up,
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
        Back(
            text=Format("◀️ Назад"),
        ),
        MessageInput(
            func=message_input_fixing,
        ),
        state=AdminOrderLookUpSG.ALL_ORDERS,
        getter=all_orders_getter,
    ),
    Window(
        Format("{order_text}"),
        Button(
            text=Format("🔄 Начать выполнение заказа"),
            id='start_fulfillment',
            on_click=switch_to_fulfillment,
            when=F['order'].status.value.in_(('NEW', 'DELAY', 'PROCESSING')),
        ),
        SwitchTo(
            text=Format("◀️ Назад"),
            id='panel_orders',
            state=AdminOrderLookUpSG.START,
        ),
        MessageInput(
            func=message_input_fixing,
        ),
        state=AdminOrderLookUpSG.ORDER_INFO,
        getter=one_order_getter,
    ),
    Window(
        Format("🔄 Не выполненные заказы ({count})", when="orders"),
        Format("На данный момент еще нет не выполненных заказов", when="is_empty"),
        ScrollingGroup(
            Select(
                id="order_select",
                items="orders",
                item_id_getter=lambda item: item.id,
                text=Format("№{item.id}"),
                on_click=selected_order_look_up,
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
        MessageInput(
            func=message_input_fixing,
        ),
        SwitchTo(
            text=Format("◀️ Назад"),
            id='panel_orders',
            state=AdminOrderLookUpSG.START,
        ),
        state=AdminOrderLookUpSG.PROCESSING_ORDERS,
        getter=processing_orders_getter,
    ),
    Window(
        Format("✅ Выполненные заказы ({count})", when="orders"),
        Format("На данный момент еще нет выполненных заказов", when="is_empty"),
        ScrollingGroup(
            Select(
                id="order_select",
                items="orders",
                item_id_getter=lambda item: item.id,
                text=Format("№{item.id}"),
                on_click=selected_order_look_up,
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
        SwitchTo(
            text=Format("◀️ Назад"),
            id='panel_orders',
            state=AdminOrderLookUpSG.START,
        ),
        MessageInput(
            func=message_input_fixing,
        ),
        state=AdminOrderLookUpSG.COMPLETED_ORDERS,
        getter=completed_orders_getter,
    ),
    Window(
        Format("На данный момент еще нет отмененных заказов", when="is_empty"),
        Format("❌ Отмененные заказы ({count})", when="orders"),
        ScrollingGroup(
            Select(
                id="order_select",
                items="orders",
                item_id_getter=lambda item: item.id,
                text=Format("№{item.id}"),
                on_click=selected_order_look_up,
                when="orders",
            ),
            id="order_group",
            height=10,
            width=2,
            hide_on_single_page=True,
            hide_pager=True,
            when="orders"
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
        SwitchTo(
            text=Format("◀️ Назад"),
            id='panel_orders',
            state=AdminOrderLookUpSG.START,
        ),
        MessageInput(
            func=message_input_fixing,
        ),
        state=AdminOrderLookUpSG.CANCELLED_ORDERS,
        getter=cancelled_orders_getter,
    ),
)
