from __future__ import annotations

import datetime
from typing import Union, Any, Optional

from src.domain.value_objects.user import (
    UserID,
    JoinedAt,
    TotalWithdrawn,
    ReferralURL,
    ReferralID,
)
from src.infrastructure.config import app_settings


class User:
    __slots__ = (
        'user_id',
        'joined_at',
        'total_withdrawn',
        'referral_id',
    )

    def __init__(
        self,
        user_id: UserID,
        joined_at: Optional[JoinedAt] = None,
        total_withdrawn: Optional[TotalWithdrawn] = None,
        referral_id: Optional[ReferralID] = None,
    ) -> None:
        self.user_id = user_id
        self.joined_at = joined_at
        self.total_withdrawn = total_withdrawn
        self.referral_id = referral_id

        if not self.total_withdrawn:
            self.total_withdrawn = TotalWithdrawn(0)
        if not self.joined_at:
            self.joined_at = JoinedAt(datetime.datetime.now(datetime.UTC))

    def __str__(self):
        return f'User <{self.user_id}>'

    def __eq__(self, other: Union[User, Any]) -> bool:
        if isinstance(other, User) and other.user_id == self.user_id:
            return True
        return False

    def get_referral_url(self) -> ReferralURL:
        return ReferralURL(f"{app_settings.bot.bot_url}/?startapp={self.user_id.value}")
