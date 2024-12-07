from src.domain.value_objects.pagination import PageNumber, Limit, Offset

class Page:
    __slots__ = ('page_number',)

    def __init__(self, page_number: PageNumber):
        self.page_number = page_number

    def get_limit(self, page_size: int) -> Limit:
        return Limit(page_size)

    def get_offset(self, page_size: int) -> Offset:
        return Offset((self.page_number.value - 1) * page_size)
