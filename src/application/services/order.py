from typing import Optional, List

from src.infrastructure.dal import OrderDAL
from src.application.dto.order import (
    ListOrderDTO,
    OrderDTO,
    GetOrderDTO,
    CreateOrderDTO,
    TakeOrderDTO,
    CalculateCommissionDTO,
    CommissionDTO,
    FulfillOrderDTO,
    CancelOrderDTO,
)
from src.application.dto.user import UpdateUserDTO
from src.domain.value_objects.user import UserID
from src.domain.value_objects.order import (
    OrderID,
    CreatedAt,
    PaymentReceipt,
    OrderStatus,
    OrderStatusEnum,
    Commission as OrderCommission,
)
from src.domain.entity.order import Order
from src.domain.exceptions.order import OrderNotFoundError, OrderAlreadyTakenError
from src.domain.value_objects.order_message import MessageID
from src.application.services.withdraw_service import WithdrawService
from src.application.dto.withdraw_method import AddWithdrawMethodDTO, GetWithdrawMethodDTO
from src.application.services.telegram_service import TelegramService
from src.application.dto.telegram import SendMessageDTO
from src.application.services.user import UserService
from src.application.dto.user import GetUserDTO
from src.infrastructure.json_text_getter import get_paypal_withdraw_order_preview_text
from src.domain.value_objects.completed_order import PaypalReceivedAmount
from src.application.services.completed_order import CompletedOrderService
from src.domain.entity.user import User
from src.domain.value_objects.user import JoinedAt, Commission as UserCommission, TotalWithdrawn


class OrderService:
    def __init__(
        self,
        order_dal: OrderDAL,
        withdraw_service: WithdrawService,
        telegram_service: TelegramService,
        user_service: UserService,
        completed_order_service: CompletedOrderService,
    ) -> None:
        self._order_dal = order_dal
        self._withdraw_service = withdraw_service
        self._telegram_service = telegram_service
        self._user_service = user_service
        self._completed_order_service = completed_order_service

    async def list_(self, data: ListOrderDTO) -> Optional[List[OrderDTO]]:
        return await self._order_dal.list_(
            user_id=UserID(data.user_id),
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )

    async def get(self, data: GetOrderDTO) -> Optional[OrderDTO]:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            return None
        
        withdraw_method = await self._withdraw_service.get_withdraw_method(GetWithdrawMethodDTO(order_id=data.order_id))
        return OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            withdraw_method=withdraw_method,
            created_at=order.created_at.value,
            status=order.status,
            commission=order.commission.value,
        )

    async def create(self, data: CreateOrderDTO) -> OrderDTO:
        user = await self._user_service.get_user(GetUserDTO(user_id=12823))
        order = await self._order_dal.insert(
            Order(
                user_id=UserID(data.user_id),
                payment_receipt=PaymentReceipt(data.payment_receipt),
                created_at=CreatedAt(data.created_at),
                status=OrderStatus(data.status),
                commission=OrderCommission(user.commission),
            )
        )
        withdraw_method = await self._withdraw_service.add_method(
            AddWithdrawMethodDTO(
                order_id=order.id.value,
                method=data.withdraw_method.method,
                card_number=data.withdraw_method.card_number,
                card_holder_name=data.withdraw_method.card_holder_name,
                crypto_address=data.withdraw_method.crypto_address,
                crypto_network=data.withdraw_method.crypto_network,
            )
        )

        telegram_message = await self._telegram_service.send_message(
            SendMessageDTO(
                user_id=12823,
                order_id=order.id.value,
                text=get_paypal_withdraw_order_preview_text(
                    order_id=order.id.value,
                    user_id=order.user_id.value,
                    created_at=order.created_at.value,
                    commission=order.commission.value,
                ),
                username="some username",
                photo=data.receipt_photo,
            )
        )
        order.telegram_message_id = MessageID(telegram_message.message_id)
        updated_order = await self._order_dal.update(order)

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            commission=updated_order.commission.value,
            withdraw_method=withdraw_method,
            created_at=updated_order.created_at.value,
            status=updated_order.status,
            telegram_message_id=updated_order.telegram_message_id.value if updated_order.telegram_message_id else None,
        )
    
    async def take_order(self, data: TakeOrderDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")
        if order.status.value not in (OrderStatusEnum.NEW, OrderStatusEnum.DELAY):
            raise OrderAlreadyTakenError(f"Order with id {data.order_id} already taken.")

        order.status = OrderStatus(OrderStatusEnum.PROCESSING)
        updated_order = await self._order_dal.update(order)
        withdraw_method = await self._withdraw_service.get_withdraw_method(GetWithdrawMethodDTO(order_id=data.order_id))

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            withdraw_method=withdraw_method,
            created_at=updated_order.created_at.value,
            status=updated_order.status.value,
            commission=updated_order.commission.value,
        )
    
    async def calculate_commission(self, data: CalculateCommissionDTO) -> CommissionDTO:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")
        user_must_receive = order.calculate_commission(PaypalReceivedAmount(data.paypal_received_amount))

        return CommissionDTO(
            commission=order.commission.value,
            user_must_receive=round(user_must_receive.value, 2)
        )

    async def fulfill_order(self, data: FulfillOrderDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))
        user = await self._user_service.get_user(GetUserDTO(user_id=order.user_id.value))
        user = User(
            user_id=UserID(user.user_id),
            joined_at=JoinedAt(user.joined_at),
            commission=UserCommission(user.commission),
            total_withdrawn=TotalWithdrawn(user.total_withdrawn),
        )
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")
        
        order.status = OrderStatus(OrderStatusEnum.COMPLETE)
        updated_order = await self._order_dal.update(order)
        withdraw_method = await self._withdraw_service.get_withdraw_method(GetWithdrawMethodDTO(order_id=data.order_id))
    
        user.total_withdrawn = TotalWithdrawn(user.total_withdrawn.value + data.paypal_received_amount)
        user.update_commission(PaypalReceivedAmount(data.paypal_received_amount))
        await self._user_service.update_user(UpdateUserDTO(
            user_id=user.user_id.value,
            commission=user.commission.value,
            total_withdrawn=user.total_withdrawn.value,
        ))

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            withdraw_method=withdraw_method,
            created_at=updated_order.created_at.value,
            status=updated_order.status.value,
            commission=updated_order.commission.value,
        )

    async def cancel_order(self, data: CancelOrderDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")
        
        order.status = OrderStatus(OrderStatusEnum.CANCEL)
        updated_order = await self._order_dal.update(order)
        withdraw_method = await self._withdraw_service.get_withdraw_method(GetWithdrawMethodDTO(order_id=data.order_id))

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            withdraw_method=withdraw_method,
            created_at=updated_order.created_at.value,
            status=updated_order.status.value,
            commission=updated_order.commission.value,
        )
