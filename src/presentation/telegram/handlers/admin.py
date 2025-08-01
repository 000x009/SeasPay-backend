from uuid import UUID

from aiogram import Router, Bot, F
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Chat, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_album.album_message import AlbumMessage

from dishka import FromDishka

from aiogram_dialog import DialogManager, StartMode, ShowMode

from src.presentation.telegram.filters import AdminFilter, ChatFilter
from src.infrastructure.json_text_getter import (
    get_paypal_order_text,
    get_admin_service_statistics_text,
    get_purchase_request_text,
)
from src.presentation.telegram.buttons import inline
from src.application.services.order import OrderService
from src.application.services.user import UserService
from src.application.services.purchase_request import PurchaseRequestService
from src.application.dto.purchase_request import TakePurchaseRequestDTO
from src.application.dto.order import TakeOrderDTO
from src.domain.exceptions.order import OrderAlreadyTakenError, OrderNotFoundError
from src.application.services.statistics import StatisticsService
from src.presentation.telegram.states import (
    OrderFulfillmentSG,
    AdminWriteUserSG,
    AdminUserOrdersSG,
    MailingSG,
    AdminOrderLookUpSG,
    AdminSearchSG,
)
from src.domain.exceptions.purchase_request import PurchaseRequestNotFound, PurchaseRequestAlreadyTaken
from src.infrastructure.config import load_bot_settings
from src.presentation.telegram.states.purchase_request import PurchaseRequestFulfillmentSG
from src.presentation.telegram.states.platform import PlatformManagementSG


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
) -> None:
    order_id = UUID(callback.data.split(':')[1])
    bot_settings = load_bot_settings()

    try:
        updated_order = await order_service.take_order(TakeOrderDTO(order_id=order_id))

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=get_paypal_order_text(
                order_id=updated_order.id,
                user_id=updated_order.user_id,
                created_at=updated_order.created_at,
                status=updated_order.status,
                order_type=updated_order.type,
            ),
            reply_markup=inline.get_order_fulfillment_kb_markup(order_id=order_id),
        )
        await bot.edit_message_text(
            chat_id=bot_settings.orders_group_id,
            message_id=updated_order.telegram_message_id,
            text=get_paypal_order_text(
                order_id=updated_order.id,
                user_id=updated_order.user_id,
                order_type=updated_order.type,
                created_at=updated_order.created_at,
                status=updated_order.status,
            ),
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
    F.data.startswith('take_purchase_request'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.SUPERGROUP),
)
async def take_product_purchase_request_handler(
    callback: CallbackQuery,
    bot: Bot,
    purchase_request_service: FromDishka[PurchaseRequestService],
) -> None:
    request_id = UUID(callback.data.split(':')[1])
    bot_settings = load_bot_settings()

    try:
        purchase_request = await purchase_request_service.take_request(TakePurchaseRequestDTO(id=request_id))
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=get_purchase_request_text(
                request_id=purchase_request.id,
                user_id=purchase_request.user_id,
                created_at=purchase_request.created_at,
                status=purchase_request.status,
                purchase_url=purchase_request.purchase_url,
            ),
            reply_markup=inline.get_purchase_request_fulfillment_kb_markup(purchase_request_id=request_id),
        )
        await bot.edit_message_text(
            chat_id=bot_settings.orders_group_id,
            message_id=purchase_request.message_id,
            text=get_purchase_request_text(
                request_id=purchase_request.id,
                user_id=purchase_request.user_id,
                created_at=purchase_request.created_at,
                status=purchase_request.status,
                purchase_url=purchase_request.purchase_url,
            ),
        )
        await callback.answer(
            'Вы успешно взялись за запрос! Вам было отправлено сообщение с информацией о запросе в личный чат с ботом.',
            show_alert=True,
        )
    except PurchaseRequestAlreadyTaken:
        await callback.answer("❌ Этот запрос уже взят другим администратором!", show_alert=True)
    except PurchaseRequestNotFound:
        await callback.answer("❌ Запрос с таким ID не был найден!", show_alert=True)


@router.callback_query(
    F.data.startswith('order_fulfillment'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def order_fulfillment_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
    state: FSMContext,
) -> None:
    order_id = callback.data.split(':')[1]
    await state.clear()
    await dialog_manager.start(
        OrderFulfillmentSG.ORDER_INFO,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
        data=dict(order_id=order_id),
    )


@router.callback_query(
    F.data.startswith('start_request_fulfillment'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def start_request_fulfillment_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    request_id = callback.data.split(':')[1]
    await dialog_manager.start(
        state=PurchaseRequestFulfillmentSG.REQUEST_INFO,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
        data=dict(request_id=request_id),
    )


# ADMIN PANEL
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
    F.data.startswith('back_apanel'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def back_apanel_handler(
    callback: CallbackQuery,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await bot.edit_message_text(
        chat_id=event_chat.id,
        message_id=callback.message.message_id,
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
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=AdminSearchSG.START,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )


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


@router.callback_query(
    F.data.startswith('admin_user_orders'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_user_orders_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
    state: FSMContext,
) -> None:
    user_id = int(callback.data.split(':')[1])
    await state.clear()
    await dialog_manager.start(
        AdminUserOrdersSG.USER_ORDERS,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
        data=dict(user_id=user_id),
    )


@router.callback_query(
    F.data.startswith('admin_mailing'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_service_statistics_handler(
    callback: CallbackQuery,
    bot: Bot,
    event_chat: Chat,
    state: FSMContext,
) -> None:
    await bot.edit_message_text(
        chat_id=event_chat.id,
        message_id=callback.message.message_id,
        text='💬 Отправьте сообщение для рассылки:',
        reply_markup=inline.back_to_apanel_kb_markup,
    )
    await state.set_state(MailingSG.MESSAGE)


@router.message(MailingSG.MESSAGE, F.media_group_id)
async def mailing_message_handler(
    album_message: AlbumMessage,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    album_photo = [message.photo[-1].file_id for message in album_message]
    media_group = MediaGroupBuilder(caption=album_message.caption)

    for photo in album_photo:
        media_group.add_photo(media=photo)

    await state.update_data(media_group=media_group)
    await bot.send_message(
        chat_id=event_chat.id,
        text="Вы уверены, что хотите разослать это сообщение всем?",
        reply_markup=inline.mailing_choice_kb_markup,
    )
    await state.set_state(MailingSG.CHECKOUT)


@router.message(MailingSG.MESSAGE)
async def mailing_message_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await state.update_data(message_id=message.message_id)
    await bot.send_message(
        chat_id=event_chat.id,
        text="Вы уверены, что хотите разослать это сообщение всем?",
        reply_markup=inline.mailing_choice_kb_markup,
    )
    await state.set_state(MailingSG.CHECKOUT)


@router.callback_query(F.data == 'confirm_mailing')
async def mailing_sender_handler(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
    user_service: FromDishka[UserService],
) -> None:
    state_data = await state.get_data()
    media_group = state_data.get("media_group")
    message_id = state_data.get("message_id")

    users = await user_service.get_all_users()
    for user in users:
        try:
            if media_group:
                await bot.send_media_group(chat_id=user.user_id, media=media_group.build())
            elif message_id:
                await bot.copy_message(
                    chat_id=user.user_id,
                    message_id=message_id,
                    from_chat_id=event_chat.id,
                )
        except Exception as ex:
            continue
    await bot.send_message(chat_id=event_chat.id, text="Сообщение успешно разослано пользователям!")
    await bot.delete_message(
        chat_id=event_chat.id,
        message_id=query.message.message_id,
    )
    await state.clear()


@router.callback_query(F.data == 'cancel_mailing')
async def mailing_sender_handler(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await state.clear()
    await bot.delete_message(chat_id=event_chat.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=event_chat.id, text="Рассылка успешно отменена")


@router.callback_query(F.data == 'admin_orders')
async def admin_orders_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
    state: FSMContext,
) -> None:
    await state.clear()
    await dialog_manager.start(
        state=AdminOrderLookUpSG.START,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )


@router.callback_query(
    F.data == 'admin_service_statistics',
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_service_statistics_handler(
    callback: CallbackQuery,
    bot: Bot,
    event_chat: Chat,
    statistics_service: FromDishka[StatisticsService]
) -> None:
    statistics = await statistics_service.get_statistics()

    await bot.edit_message_text(
        chat_id=event_chat.id,
        message_id=callback.message.message_id,
        text=get_admin_service_statistics_text(
            all_time_profit=statistics.profit.all_time,
            month_profit=statistics.profit.month,
            week_profit=statistics.profit.week,
            all_users_amount=statistics.new_users.all,
            new_month_users=statistics.new_users.month,
            new_week_users=statistics.new_users.week,
            new_day_users=statistics.new_users.day,
            total_withdrawn=statistics.total_withdrawn,
        ),
        reply_markup=inline.back_to_apanel_kb_markup,
    )


@router.callback_query(
    F.data == 'admin_products',
    AdminFilter(),
    ChatFilter(chat_type=ChatType.PRIVATE),
)
async def admin_products_handler(
    callback: CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=PlatformManagementSG.PLATFORM_LIST,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )
