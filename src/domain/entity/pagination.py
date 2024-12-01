from src.domain.value_objects.pagination import PageNumber, Limit, Offset

PAGE_SIZE = 5


class Page:
    __slots__ = ('page_number',)

    def __init__(self, page_number: PageNumber):
        self.page_number = page_number

    def get_limit(self) -> Limit:
        return Limit(PAGE_SIZE)

    def get_offset(self) -> Offset:
        return Offset((self.page_number.value - 1) * PAGE_SIZE)
