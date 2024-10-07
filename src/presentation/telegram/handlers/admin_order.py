from aiogram import Router, Bot, F
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Chat, Message
from aiogram.fsm.context import FSMContext

from dishka import FromDishka

from aiogram_dialog import DialogManager, StartMode, ShowMode, Data

from src.presentation.telegram.filters import AdminFilter, ChatFilter
from src.infrastructure.json_text_getter import (
    get_paypal_withdraw_order_text,
    get_order_commission_form_text,
    get_withdraw_card_text,
)
from src.presentation.telegram.buttons import inline
from src.application.services.order import OrderService
from src.application.services.user import UserService
from src.application.dto.order import GetOrderDTO, TakeOrderDTO
from src.application.dto.user import GetUserDTO
from src.domain.exceptions.order import OrderAlreadyTakenError, OrderNotFoundError
from src.infrastructure.config import load_bot_settings
from src.presentation.telegram.states.admin_order import OrderFulfillmentSG


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
