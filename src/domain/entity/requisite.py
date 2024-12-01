from typing import Optional
from datetime import datetime
from uuid import uuid4

from src.domain.entity.user import UserID
from src.domain.value_objects.requisite import RequisiteId, RequisiteType, CreatedAt


class Requisite:
    __slots__ = (
        "id",
        "user_id",
        "type",
        "created_at",
    )

    def __init__(
        self,
        user_id: UserID,
        type: RequisiteType,
        id: Optional[RequisiteId] = None,
        created_at: Optional[CreatedAt] = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.type = type
        self.created_at = created_at

        if not self.id:
            self.id = RequisiteId(uuid4())
        if not self.created_at:
            self.created_at = CreatedAt(datetime.now())
