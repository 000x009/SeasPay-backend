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
from aiogram_dialog.widgets.input import MessageInput, TextInput

from src.presentation.telegram.dialogs.admin.getter import (
    order_getter,
    one_order_getter,
    all_orders_getter,
    processing_orders_getter,
    completed_orders_getter,
    cancelled_orders_getter,
    user_getter,
    message_getter,
    user_orders_getter,
)
from src.presentation.telegram.dialogs.common.handler import message_input_fixing
from src.presentation.telegram.states import AdminUserOrdersSG, AdminOrderLookUpSG, AdminSearchSG
from src.presentation.telegram.dialogs.admin.handlers import (
    selected_order,
    selected_order_look_up,
    switch_to_fulfillment,
    on_user_id,
    on_order_id,
    on_message_to_user,
    confirm_message_sending,
    selected_user_order,
)


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
            when=F['order'].status.in_(('NEW', 'DELAY', 'PROCESSING')),
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


admin_search_dialog = Dialog(
    Window(
        Const('Выберите, что вы желаете найти по кнопкам ниже'),
        SwitchTo(
            text=Const('👤 Пользователь'),
            state=AdminSearchSG.USER_SEARCH,
            id='user_search_switch'
        ),
        SwitchTo(
            text=Const('🛒 Заказ'),
            state=AdminSearchSG.ORDER_SEARCH,
            id='order_search_switch'
        ),
        MessageInput(
            func=message_input_fixing,
        ),
        state=AdminSearchSG.START,
    ),
    Window(
        Const('Напишите ID пользователя для просмотра информации о нем...'),
        TextInput(
            id='user_id_input',
            on_success=on_user_id,
        ),
        SwitchTo(
            text=Format("◀️ Назад"),
            id='back_to_panel',
            state=AdminSearchSG.START,
        ),
        state=AdminSearchSG.USER_SEARCH,
    ),
    Window(
        Const('Напишите ID заказа для просмотра информации о нем...'),
        TextInput(
            id='order_id_input',
            on_success=on_order_id,
        ),
        SwitchTo(
            text=Format("◀️ Назад"),
            id='back_to_panel',
            state=AdminSearchSG.START,
        ),
        state=AdminSearchSG.ORDER_SEARCH,
    ),
    Window(
        Format('{user_text}', when='user'),
        Const('Пользователь с данным ID не был найден...', when='is_empty'),
        MessageInput(
            func=message_input_fixing,
        ),
        SwitchTo(
            text=Const('📨 Отправить сообщение'),
            id='switch_to_write_user',
            state=AdminSearchSG.WRITE_TO_USER,
        ),
        SwitchTo(
            text=Const('🛒 История заказов'),
            state=AdminSearchSG.USER_ORDERS,
            id='user_orders',
        ),
        SwitchTo(
            text=Format("◀️ Назад"),
            id='search_user',
            state=AdminSearchSG.USER_SEARCH,
        ),
        state=AdminSearchSG.USER,
        getter=user_getter,
    ),
    Window(
        Format("{order_text}"),
        Const('Заказ с данным ID не был найден...', when='is_empty'),
        Button(
            text=Format("🔄 Начать выполнение заказа"),
            id='start_fulfillment',
            on_click=switch_to_fulfillment,
            when=F['order'].status.in_(('NEW', 'DELAY', 'PROCESSING')),
        ),
        SwitchTo(
            text=Format("◀️ Назад"),
            id='panel_orders',
            state=AdminSearchSG.START,
        ),
        MessageInput(
            func=message_input_fixing,
        ),
        state=AdminSearchSG.ORDER,
        getter=one_order_getter,
    ),
    Window(
        Const('Введите сообщение, которое желаете отправить пользователю...'),
        TextInput(
            id='user_message',
            on_success=on_message_to_user,
        ),
        SwitchTo(
            text=Format("◀️ Назад"),
            id='panel_orders',
            state=AdminSearchSG.USER,
        ),
        state=AdminSearchSG.WRITE_TO_USER
    ),
    Window(
        Format('Вы уверенны, что желаете отправить это сообщение пользователю?\n\n<blockquote>{message}</blockquote>'),
        Button(
            text=Const('✅ Да'),
            id='confirm_sending',
            on_click=confirm_message_sending,
        ),
        SwitchTo(
            text=Format("◀️ Назад"),
            id='wite_user_back',
            state=AdminSearchSG.WRITE_TO_USER,
        ),
        state=AdminSearchSG.PRE_CONFIRM_MESSAGE,
        getter=message_getter,
    ),
    Window(
        Const('Заказы пользователя:', when='orders'),
        Const('У пользователя нет заказов', when='is_empty'),
        ScrollingGroup(
            Select(
                id="order_select",
                items="orders",
                item_id_getter=lambda item: item.id,
                text=Format("№{item.id}"),
                on_click=selected_user_order,
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
            id='back_to_user',
            state=AdminSearchSG.USER,
        ),
        MessageInput(
            func=message_input_fixing,
        ),
        state=AdminSearchSG.USER_ORDERS,
        getter=user_orders_getter,
    ),
    Window(
        Format("{order_text}"),
        Back(
            text=Format("◀️ Назад"),
        ),
        state=AdminSearchSG.USER_ORDER,
        getter=one_order_getter,
    )
)
