
from enum import StrEnum, auto


class OrderStatus(StrEnum):
    PENDING = auto()
    PAYED = auto()
    DELIVERED = auto()
