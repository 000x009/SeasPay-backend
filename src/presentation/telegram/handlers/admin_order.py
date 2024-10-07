from aiogram import Router, Bot, F
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Chat, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from dishka import FromDishka

from aiogram_dialog import DialogManager, StartMode

from src.presentation.telegram.filters import AdminFilter, ChatFilter
from src.infrastructure.json_text_getter import (
    get_paypal_withdraw_order_text,
    get_user_profile_text,
)
from src.presentation.telegram.buttons import inline
from src.application.services.order import OrderService
from src.application.services.user import UserService
from src.application.dto.order import GetOrderDTO, TakeOrderDTO
from src.application.dto.user import GetUserDTO
from src.domain.exceptions.order import OrderAlreadyTakenError, OrderNotFoundError
from src.presentation.telegram.states import (
    OrderFulfillmentSG,
    AdminSearchUserSG,
    AdminWriteUserSG,
    AdminUserOrdersSG,
)


router = Router()

@router.callback_query(
    F.data.startswith('take_order'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.SUPERGROUP),
)
async def take_order_handler(
    callback: CallbackQuery,
    bot: Bot,
    order_service: FromDishka[OrderService],
    user_service: FromDishka[UserService],
) -> None:
    order_id = int(callback.data.split(':')[1])
    order = await order_service.get(GetOrderDTO(order_id=order_id))
    customer = await user_service.get_user(GetUserDTO(user_id=order.user_id))

    try:
        updated_order = await order_service.take_order(TakeOrderDTO(order_id=order_id))
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=get_paypal_withdraw_order_text(
                order_id=updated_order.id,
                user_id=updated_order.user_id,
                created_at=updated_order.created_at,
                status=updated_order.status.value,
                commission=customer.commission,
            ),
            reply_markup=inline.get_order_fulfillment_kb_markup(order_id=order_id),
        )
        await callback.answer(
            'Вы успешно взялись за заказ! Вам было отправлено сообщение с информацией о заказе в личный чат с ботом.',
            show_alert=True,
        )
    except OrderAlreadyTakenError:
        await callback.answer("❌ Этот заказ уже взят другим администратором!", show_alert=True)
    except OrderNotFoundError:
        await callback.answer("❌ Заказ с таким ID не был найден!", show_alert=True)


@router.callback_query(
    F.data.startswith('order_fulfillment'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def order_fulfillment_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    order_id = callback.data.split(':')[1]
    await dialog_manager.start(
        OrderFulfillmentSG.ORDER_INFO,
        mode=StartMode.RESET_STACK,
        data=dict(order_id=int(order_id)),
    )


#ADMIN PANEL
@router.message(
    Command('admin'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_panel_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await bot.send_message(
        chat_id=event_chat.id,
        text='👮‍♂️ Выберите действия ниже в админ-панели:',
        reply_markup=inline.get_admin_panel_kb_markup(),
    )


@router.callback_query(
    F.data.startswith('admin_search_user'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_search_user_handler(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    event_chat: Chat,
) -> None:
    await bot.edit_message_text(
        chat_id=event_chat.id,
        message_id=callback.message.message_id,
        text='🔍 Введите ID пользователя для просмотра его профиля:',
    )
    await state.set_state(AdminSearchUserSG.SEARCH_USER)


@router.message(
    AdminSearchUserSG.SEARCH_USER,
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_search_user_handler(
    message: Message,
    bot: Bot,
    user_service: FromDishka[UserService],
    state: FSMContext,
) -> None:
    user_id = int(message.text)
    try:
        user = await user_service.get_user(GetUserDTO(user_id=user_id))
        if user:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=get_user_profile_text(
                    user_id=user.user_id,
                    commission=user.commission,
                    total_withdrawn=user.total_withdrawn,
                ),
                reply_markup=inline.get_user_profile_kb_markup(user_id=user_id),
            )
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text='❌ Пользователь с таким ID не был найден!',
            )
    finally:
        await state.clear()


@router.callback_query(
    F.data.startswith('admin_write_user'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_write_user_handler(
    callback: CallbackQuery,
    bot: Bot,
    event_chat: Chat,
    state: FSMContext,
) -> None:
    user_id = int(callback.data.split(':')[1])
    await state.update_data(user_id=user_id)
    await bot.send_message(
        chat_id=event_chat.id,
        text='💬 Введите сообщение для пользователя:',
    )
    await state.set_state(AdminWriteUserSG.WRITE_USER)


@router.message(
    AdminWriteUserSG.WRITE_USER,
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_write_user_handler(
    message: Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    user_id = (await state.get_data())['user_id']
    await bot.send_message(
        chat_id=user_id,
        text=message.text,
    )
    await message.answer('✅ Сообщение было отправлено пользователю!')
    await state.clear()


#TODO:
@router.callback_query(
    F.data.startswith('admin_user_orders'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_user_orders_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    user_id = int(callback.data.split(':')[1])
    await dialog_manager.start(
        AdminUserOrdersSG.USER_ORDERS,
        mode=StartMode.RESET_STACK,
        data=dict(user_id=user_id),
    )
