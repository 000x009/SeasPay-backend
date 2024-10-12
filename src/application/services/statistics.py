from src.application.services.completed_order import CompletedOrderService
from src.application.services.user import UserService
from src.application.dto.statistics import StatisticsDTO, StatisticsProfitDTO, NewUsersDTO


class StatisticsService:
    def __init__(
        self,
        completed_order_service: CompletedOrderService,
        user_service: UserService,
    ) -> None:
        self.completed_order_service = completed_order_service
        self.user_service = user_service

    async def get_statistics(self) -> StatisticsDTO:
        profit = await self.completed_order_service.count_statistics_profit()
        total_withdrawn = await self.completed_order_service.count_total_withdraw()
        new_users = await self.user_service.get_new_users_statistics()

        return StatisticsDTO(
            profit=StatisticsProfitDTO(
                all_time=profit.all_time,
                month=profit.month,
                week=profit.week,
            ),
            new_users=NewUsersDTO(
                all=new_users.all,
                month=new_users.month,
                week=new_users.week,
                day=new_users.day,
            ),
            total_withdrawn=total_withdrawn.total_withdraw,
        )
