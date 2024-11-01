from typing import Optional, List

from src.infrastructure.dal import UserDAL
from src.application.dto.user import (
    CreateUserDTO,
    GetUserDTO,
    UserDTO,
    UpdateUserDTO,
    NewUsersDTO,
)
from src.domain.entity.user import User
from src.domain.value_objects.user import UserID, JoinedAt, TotalWithdrawn
from src.domain.exceptions.user import UserNotFoundError
from src.domain.value_objects.statistics import TimeSpan
from src.application.common.uow import UoW
from src.application.services.user_commission import UserCommissionService
from src.application.dto.user_commission import CreateUserCommissionDTO
from src.infrastructure.config import app_settings


class UserService:
    def __init__(
        self,
        user_dal: UserDAL,
        uow: UoW,
        user_commission_service: UserCommissionService,
    ) -> None:
        self._user_dal = user_dal
        self.uow = uow
        self.user_commission_service = user_commission_service

    async def add(self, data: CreateUserDTO) -> UserDTO:
        user = await self._user_dal.insert(User(UserID(data.user_id)))
        await self.user_commission_service.add(CreateUserCommissionDTO(
            user_id=data.user_id,
            transfer=app_settings.commission.max_transfer_percentage,
            withdraw=app_settings.commission.max_withdraw_percentage,
            digital_product=app_settings.commission.digital_product_usd_amount_commission,
        ))
        await self.uow.commit()

        return UserDTO(
            user_id=user.user_id.value,
            joined_at=user.joined_at.value,
            total_withdrawn=user.total_withdrawn.value
        )
    
    async def get_user(self, data: GetUserDTO) -> Optional[UserDTO]:
        user = await self._user_dal.get_one(UserID(data.user_id))
        if user is None:
            return None
        
        return UserDTO(
            user_id=user.user_id.value,
            joined_at=user.joined_at.value,
            total_withdrawn=user.total_withdrawn.value
        )

    async def get_all_users(self) -> List[UserDTO]:
        users = await self._user_dal.get_all_users()

        return [UserDTO(
            user_id=user.user_id.value,
            joined_at=user.joined_at.value,
            total_withdrawn=user.total_withdrawn.value
        ) for user in users]
    
    async def update_user(self, data: UpdateUserDTO) -> None:
        user = await self._user_dal.get_one(UserID(data.user_id))
        if user is None:
            raise UserNotFoundError(f"User with id {data.user_id} not found.")

        await self._user_dal.update(UserID(data.user_id), User(
            user_id=UserID(data.user_id),
            joined_at=JoinedAt(user.joined_at.value),
            total_withdrawn=TotalWithdrawn(data.total_withdrawn)
        ))
        await self.uow.commit()

    async def get_new_users_statistics(self) -> NewUsersDTO:
        all_users = await self._user_dal.get_new_users_amount()
        month_users = await self._user_dal.get_new_users_amount(TimeSpan(30))
        week_users = await self._user_dal.get_new_users_amount(TimeSpan(7))
        day_users = await self._user_dal.get_new_users_amount(TimeSpan(1))

        return NewUsersDTO(
            all=all_users,
            month=month_users,
            week=week_users,
            day=day_users,
        )
