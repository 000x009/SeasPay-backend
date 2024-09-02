from dataclasses import dataclass



@dataclass(frozen=True)
class SendOrderDTO:
    user_id: int
    username: str
    order_text: str
    