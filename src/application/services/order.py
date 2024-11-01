import uuid
from typing import Optional, List

from src.infrastructure.dal import OrderDAL
from src.application.common.dto import FileDTO
from src.application.dto.order import (
    ListOrderDTO,
    OrderDTO,
    GetOrderDTO,
    CreateWithdrawOrderDTO,
    TakeOrderDTO,
    FulfillWithdrawOrderDTO,
    CancelOrderDTO,
    CreateTransferOrderDTO,
    FulfillTransferOrderDTO,
    CreateDigitalProductOrderDTO,
    FulfillDigitalProductOrderDTO,
)
from src.application.dto.user import UpdateUserDTO
from src.domain.value_objects.user import UserID
from src.domain.value_objects.order import (
    OrderID,
    CreatedAt,
    PaymentReceipt,
    OrderStatus,
    OrderStatusEnum,
    OrderType,
    OrderTypeEnum,
)
from src.domain.entity.order import Order
from src.domain.exceptions.order import OrderNotFoundError, OrderAlreadyTakenError
from src.domain.value_objects.order_message import MessageID
from src.application.services.withdraw_details import WithdrawService
from src.application.services.transfer_details import TransferDetailsService
from src.application.dto.withdraw_details import AddWithdrawDetailsDTO, GetWithdrawDetailsDTO
from src.application.services.telegram_service import TelegramService
from src.application.dto.telegram import SendMessageDTO
from src.application.services.user import UserService
from src.application.dto.completed_order import AddCompletedOrderDTO
from src.application.dto.user import GetUserDTO
from src.infrastructure.json_text_getter import get_paypal_order_text
from src.application.services.completed_order import CompletedOrderService
from src.domain.entity.user import User
from src.domain.value_objects.user import JoinedAt, TotalWithdrawn
from src.application.common.uow import UoW
from src.application.common.cloud_storage import CloudStorage
from src.domain.value_objects.yandex_cloud import Bucket, ObjectKey
from src.infrastructure.config import load_settings
from src.application.dto.transfer_details import AddTransferDetailsDTO
from src.application.services.user_commission import UserCommissionService
from src.application.dto.user_commission import GetUserCommissionDTO, UpdateUserCommissionDTO
from src.domain.entity.user_commission import UserCommission
from src.domain.value_objects.user_commission import (
    UserTransferCommission,
    UserWithdrawCommission,
    UserDigitalProductCommission
)
from src.application.dto.product_application import FulfillProductApplicationDTO
from src.application.services.product_application import ProductApplicationService
from src.infrastructure.config import app_settings
from src.application.services.digital_product_details import DigitalProductDetailsService
from src.application.dto.digital_product_details import AddDigitalProductDetailsDTO
from src.application.services.purchase_request import PurchaseRequestService
from src.application.dto.purchase_request import GetOnePurchaseRequestDTO


class OrderService:
    def __init__(
        self,
        order_dal: OrderDAL,
        withdraw_service: WithdrawService,
        transfer_service: TransferDetailsService,
        telegram_service: TelegramService,
        user_service: UserService,
        completed_order_service: CompletedOrderService,
        uow: UoW,
        cloud_storage: CloudStorage,
        user_commission_service: UserCommissionService,
        product_application_service: ProductApplicationService,
        digital_product_details_service: DigitalProductDetailsService,
        purchase_request_service: PurchaseRequestService,
    ) -> None:
        self._order_dal = order_dal
        self._withdraw_service = withdraw_service
        self._telegram_service = telegram_service
        self._user_service = user_service
        self._completed_order_service = completed_order_service
        self.uow = uow
        self.cloud_storage = cloud_storage
        self.transfer_service = transfer_service
        self.user_commission_service = user_commission_service
        self.product_application_service = product_application_service
        self.digital_product_details_service = digital_product_details_service
        self.purchase_request_service = purchase_request_service

    async def create_digital_product_order(self, data: CreateDigitalProductOrderDTO) -> OrderDTO:
        application = await self.product_application_service.fulfill_application(FulfillProductApplicationDTO(
            id=data.application_id
        ))
        purchase_request = await self.purchase_request_service.get_request(GetOnePurchaseRequestDTO(
            application.purchase_request_id
        ))
        order = await self._order_dal.insert(
            Order(
                id=OrderID(uuid.uuid4()),
                user_id=UserID(application.user_id),
                payment_receipt=PaymentReceipt(data.payment_receipt_url),
                type_=OrderType(OrderTypeEnum.DIGITAL_PRODUCT),
            )
        )
        await self.digital_product_details_service.insert(AddDigitalProductDetailsDTO(
            order_id=order.id.value,
            commission=app_settings.commission.digital_product_usd_amount_commission,
            purchase_url=purchase_request.purchase_url,
            login_data=data.login_data,
        ))
        payment_receipt_object = self.cloud_storage.get_object_file(
            Bucket(app_settings.cloud_settings.receipts_bucket_name),
            ObjectKey(data.payment_receipt_url.split('/')[-1])
        )
        telegram_message = await self._telegram_service.send_message(
            SendMessageDTO(
                user_id=data.user_id,
                order_id=order.id.value,
                text=get_paypal_order_text(
                    order_id=order.id.value,
                    user_id=order.user_id.value,
                    created_at=order.created_at.value,
                    status=order.status.value,
                    order_type=order.type_.value,
                ),
                username=data.username,
                photo=FileDTO(
                    filename=data.payment_receipt_url.split('/')[-1],
                    input_file=payment_receipt_object.file.value,
                )
            )
        )
        order.telegram_message_id = MessageID(telegram_message.message_id)
        updated_order = await self._order_dal.update(order)
        await self.uow.commit()

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            type=updated_order.type_.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status,
            telegram_message_id=updated_order.telegram_message_id.value,
        )

    async def list_orders(self, data: ListOrderDTO) -> Optional[List[OrderDTO]]:
        orders = await self._order_dal.list_(
            user_id=UserID(data.user_id),
            limit=data.pagination.limit if data.pagination else None,
            offset=data.pagination.offset if data.pagination else None,
        )
        if not orders:
            return None
        
        return [OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            type=order.type_.value,
            created_at=order.created_at.value,
            status=order.status.value,
            telegram_message_id=order.telegram_message_id.value,
        ) for order in orders]

    async def get(self, data: GetOrderDTO) -> Optional[OrderDTO]:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            return None

        return OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            type=order.type_.value,
            created_at=order.created_at.value,
            status=order.status.value,
            telegram_message_id=order.telegram_message_id.value,
        )

    async def create_withdraw_order(self, data: CreateWithdrawOrderDTO) -> OrderDTO:
        settings = load_settings()
        user_commission = await self.user_commission_service.get(GetUserCommissionDTO(
            user_id=data.user_id,
        ))
        order = await self._order_dal.insert(
            Order(
                id=OrderID(uuid.uuid4()),
                user_id=UserID(data.user_id),
                payment_receipt=PaymentReceipt(data.payment_receipt_url),
                created_at=CreatedAt(data.created_at),
                status=OrderStatus(data.status),
                type_=OrderType(OrderTypeEnum.WITHDRAW),
            )
        )
        await self._withdraw_service.add_method(
            AddWithdrawDetailsDTO(
                order_id=order.id.value,
                payment_receipt=data.payment_receipt_url,
                commission=user_commission.withdraw,
                method=data.method,
                card_number=data.card_number,
                card_holder_name=data.card_holder_name,
                crypto_address=data.crypto_address,
                crypto_network=data.crypto_network,
            )
        )
        payment_receipt_object = self.cloud_storage.get_object_file(
            Bucket(settings.cloud_settings.receipts_bucket_name),
            ObjectKey(data.payment_receipt_url.split('/')[-1])
        )
        telegram_message = await self._telegram_service.send_message(
            SendMessageDTO(
                user_id=data.user_id,
                order_id=order.id.value,
                text=get_paypal_order_text(
                    order_id=order.id.value,
                    user_id=order.user_id.value,
                    created_at=order.created_at.value,
                    status=order.status.value,
                    order_type=order.type_.value,
                ),
                username=data.username,
                photo=FileDTO(
                    filename=data.payment_receipt_url.split('/')[-1],
                    input_file=payment_receipt_object.file.value,
                )
            )
        )
        order.telegram_message_id = MessageID(telegram_message.message_id)
        updated_order = await self._order_dal.update(order)
        await self.uow.commit()

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            type=updated_order.type_.value,
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
        await self.uow.commit()

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            type=updated_order.type_.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status.value,
            telegram_message_id=updated_order.telegram_message_id.value,
        )

    async def fulfill_withdraw_order(self, data: FulfillWithdrawOrderDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))
        user = await self._user_service.get_user(GetUserDTO(user_id=order.user_id.value))
        user_commission = await self.user_commission_service.get(GetUserCommissionDTO(user_id=user.user_id))
        user_commission = UserCommission(
            user_id=UserID(user.user_id),
            transfer=UserTransferCommission(user_commission.transfer),
            withdraw=UserWithdrawCommission(user_commission.withdraw),
            digital_product=UserDigitalProductCommission(user_commission.digital_product),
        )
        user = User(
            user_id=UserID(user.user_id),
            joined_at=JoinedAt(user.joined_at),
            total_withdrawn=TotalWithdrawn(user.total_withdrawn),
        )
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")

        order.status = OrderStatus(OrderStatusEnum.COMPLETE)
        updated_order = await self._order_dal.update(order)

        user.total_withdrawn = TotalWithdrawn(user.total_withdrawn.value + data.payment_system_received_amount)
        user_commission.update_withdraw_commission(user_total_withdrawn=user.total_withdrawn)
        await self.user_commission_service.update(UpdateUserCommissionDTO(
            user_id=user.user_id.value,
            transfer=user_commission.transfer.value,
            withdraw=user_commission.withdraw.value,
            digital_product=user_commission.digital_product.value,
        ))
        await self._user_service.update_user(UpdateUserDTO(
            user_id=user.user_id.value,
            total_withdrawn=user.total_withdrawn.value,
        ))
        await self._completed_order_service.add(AddCompletedOrderDTO(
            order_id=updated_order.id.value,
            payment_system_received_amount=data.payment_system_received_amount,
            user_received_amount=data.user_received_amount,
        ))
        await self.uow.commit()

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            type=updated_order.type_.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status.value,
            telegram_message_id=updated_order.telegram_message_id.value,
        )

    async def fulfill_digital_product_order(self, data: FulfillDigitalProductOrderDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")

        order.status = OrderStatus(OrderStatusEnum.COMPLETE)
        updated_order = await self._order_dal.update(order)

        await self._completed_order_service.add(AddCompletedOrderDTO(
            order_id=updated_order.id.value,
        ))
        await self.uow.commit()

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            type=updated_order.type_.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status.value,
            telegram_message_id=updated_order.telegram_message_id.value,
        )
    
    async def fulfill_transfer_order(self, data: FulfillTransferOrderDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")
        
        order.status = OrderStatus(OrderStatusEnum.COMPLETE)
        updated_order = await self._order_dal.update(order)
        await self._completed_order_service.add(AddCompletedOrderDTO(order_id=updated_order.id.value))
        await self.uow.commit()

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            type=updated_order.type_.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status.value,
            telegram_message_id=updated_order.telegram_message_id.value,
        )

    async def cancel_order(self, data: CancelOrderDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")
        
        order.status = OrderStatus(OrderStatusEnum.CANCEL)
        updated_order = await self._order_dal.update(order)
        await self._withdraw_service.get_withdraw_method(GetWithdrawDetailsDTO(order_id=data.order_id))
        await self.uow.commit()

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            type=updated_order.type_.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status.value,
            telegram_message_id=updated_order.telegram_message_id.value,
        )

    async def get_all_orders(self) -> Optional[List[OrderDTO]]:
        orders = await self._order_dal.list_all()
        if not orders:
            return None
        
        return [OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            type=order.type_.value,
            created_at=order.created_at.value,
            status=order.status.value,
            telegram_message_id=order.telegram_message_id.value,
        ) for order in orders]

    async def get_processing_orders(self) -> Optional[List[OrderDTO]]:
        orders = await self._order_dal.list_processing()
        if not orders:
            return None
        
        return [OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            type=order.type_.value,
            created_at=order.created_at.value,
            status=order.status.value,
            telegram_message_id=order.telegram_message_id.value
        ) for order in orders]

    async def get_completed_orders(self) -> Optional[List[OrderDTO]]:
        orders = await self._order_dal.list_completed()
        if not orders:
            return None
        
        return [OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            created_at=order.created_at.value,
            status=order.status.value,
            type=order.type_.value,
            telegram_message_id=order.telegram_message_id.value
        ) for order in orders]

    async def get_cancelled_orders(self) -> Optional[List[OrderDTO]]:
        orders = await self._order_dal.list_cancelled()
        if not orders:
            return None
        
        return [OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            type=order.type_.value,
            created_at=order.created_at.value,
            status=order.status.value,
            telegram_message_id=order.telegram_message_id.value
        ) for order in orders]

    async def create_transfer_order(self, data: CreateTransferOrderDTO) -> OrderDTO:
        settings = load_settings()
        await self._user_service.get_user(GetUserDTO(user_id=data.user_id))
        order = await self._order_dal.insert(
            Order(
                id=OrderID(uuid.uuid4()),
                user_id=UserID(data.user_id),
                payment_receipt=PaymentReceipt(data.payment_receipt_url),
                created_at=CreatedAt(data.created_at),
                type_=OrderType(OrderTypeEnum.TRANSFER),
            )
        )
        user_commission = await self.user_commission_service.get(GetUserCommissionDTO(user_id=data.user_id))
        await self.transfer_service.add_details(
            AddTransferDetailsDTO(
                order_id=order.id.value,
                receiver_email=data.receiver_email,
                amount=data.transfer_amount,
                receipt_photo_url=data.payment_receipt_url,
                commission=user_commission.transfer,
            )
        )
        payment_receipt_object = self.cloud_storage.get_object_file(
            Bucket(settings.cloud_settings.receipts_bucket_name),
            ObjectKey(data.payment_receipt_url.split('/')[-1])
        )
        telegram_message = await self._telegram_service.send_message(
            SendMessageDTO(
                user_id=data.user_id,
                order_id=order.id.value,
                text=get_paypal_order_text(
                    order_id=order.id.value,
                    user_id=order.user_id.value,
                    created_at=order.created_at.value,
                    status=order.status.value,
                    order_type=order.type_.value,
                ),
                username=data.username,
                photo=FileDTO(
                    filename=data.payment_receipt_url.split('/')[-1],
                    input_file=payment_receipt_object.file.value,
                )
            )
        )
        order.telegram_message_id = MessageID(telegram_message.message_id)
        updated_order = await self._order_dal.update(order)
        await self.uow.commit()

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            type=updated_order.type_.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status,
            telegram_message_id=updated_order.telegram_message_id.value if updated_order.telegram_message_id else None,
        )
