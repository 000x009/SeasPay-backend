from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.application.common.dto import FileDTO


@dataclass(frozen=True)
class SendMessageDTO:
    user_id: int
    username: str
    order_id: UUID
    text: str
    is_paid: bool = field(default=True)
    photo: Optional[FileDTO] = field(default=None)


@dataclass(frozen=True)
class MakeOrderPaidDTO:
    order_id: UUID
    text: str
    message_id: int


@dataclass(frozen=True)
class SendPurchaseRequestMessageDTO:
    user_id: int
    username: str
    request_id: UUID
    text: str
    photo: Optional[FileDTO] = field(default=None)

@dataclass(frozen=True)
class SavePreparedInlineMessageDTO:
    user_id: int
    title: str
    message_text: str


@dataclass(frozen=True)
class PreparedInlineMessageDTO:
    prepared_message_id: str


@dataclass(frozen=True)
class SendMessageToUserDTO:
    user_id: int
    message: str
