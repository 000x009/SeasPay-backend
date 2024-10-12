from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class StatisticsProfitDTO:
    all_time: Decimal
    month: Decimal
    week: Decimal


@dataclass(frozen=True)
class NewUsersDTO:
    """New users for a month, week, day and how many in general"""

    all: int
    month: int
    week: int
    day: int


@dataclass(frozen=True)
class StatisticsDTO:
    profit: StatisticsProfitDTO
    new_users: NewUsersDTO
    total_withdrawn: Decimal
