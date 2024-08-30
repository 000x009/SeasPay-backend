from typing import Optional, List

from src.infrastructure.dal import UserDAL
from src.application.dto.user import CreateUserDTO, GetUserDTO, UserDTO, UpdateUserCommissionDTO, UpdateUserTotalWithdrawnDTO
from src.domain.entity.user import User
from src.domain.value_objects.user import UserID, JoinedAt, Commission, TotalWithdrawn
from src.domain.exceptions.user import UserNotFoundError


class UserService:
    def __init__(self, user_dal: UserDAL) -> None:
        self._user_dal = user_dal

    async def add(self, data: CreateUserDTO) -> UserDTO:
        user = await self._user_dal.insert(User(
            user_id=UserID(data.user_id),
            joined_at=JoinedAt(data.joined_at),
            commission=Commission(data.commission),
            total_withdrawn=TotalWithdrawn(data.total_withdrawn)
        ))

        return UserDTO(
            user_id=user.user_id.value,
            joined_at=user.joined_at.value,
            commission=user.commission.value,
            total_withdrawn=user.total_withdrawn.value
        )
    
    async def get_user(self, data: GetUserDTO) -> Optional[UserDTO]:
        user = await self._user_dal.get_one(UserID(data.user_id))
        if user is None:
            return None
        
        return UserDTO(
            user_id=user.user_id.value,
            joined_at=user.joined_at.value,
            commission=user.commission.value,
            total_withdrawn=user.total_withdrawn.value
        )

    async def get_all_users(self) -> List[UserDTO]:
        users = await self._user_dal.get_all_users()

        return [UserDTO(
            user_id=user.user_id.value,
            joined_at=user.joined_at.value,
            commission=user.commission.value,
            total_withdrawn=user.total_withdrawn.value
        ) for user in users]
    
    async def update_commission(self, data: UpdateUserCommissionDTO) -> None:
        user = await self._user_dal.get_one(UserID(data.user_id))
        if user is None:
            raise UserNotFoundError(f"User with id {data.user_id} not found.")

        await self._user_dal.update(UserID(data.user_id), User(
            user_id=UserID(data.user_id),
            joined_at=JoinedAt(user.joined_at.value),
            commission=Commission(data.commission),
            total_withdrawn=TotalWithdrawn(user.total_withdrawn.value)
        ))
    
    async def update_total_withdrawn(self, data: UpdateUserTotalWithdrawnDTO) -> None:
        user = await self._user_dal.get_one(UserID(data.user_id))
        if user is None:
            raise UserNotFoundError(f"User with id {data.user_id} not found.")

        await self._user_dal.update(UserID(data.user_id), User(
            user_id=UserID(data.user_id),
            joined_at=JoinedAt(user.joined_at.value),
            commission=Commission(user.commission.value),
            total_withdrawn=TotalWithdrawn(data.total_withdrawn)))
        