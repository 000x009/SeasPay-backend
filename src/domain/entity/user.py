from __future__ import annotations
from typing import Union, Any

from src.domain.value_objects.user import UserID, UserJoinedAt, UserCommission, UserTotalWithdrawn


class User:
    __slots__ = (
        'user_id',
        'joined_at',
        'commission',
        'total_withdrawn',
    )

    def __init__(
        self,
        user_id: UserID,
        joined_at: UserJoinedAt,
        commission: UserCommission,
        total_withdrawn: UserTotalWithdrawn,
    ) -> None:
        self.user_id = user_id
        self.joined_at = joined_at
        self.commission = commission
        self.total_withdrawn = total_withdrawn

    def __str__(self):
        return f'User <{self.user_id}>'

    def __eq__(self, other: Union[User, Any]) -> bool:
        if isinstance(other, User) and other.user_id == self.user_id:
            return True
        return False
