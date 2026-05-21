from pydantic import BaseModel
from datetime import datetime, date

from enum import StrEnum, auto


class OrderStatus(StrEnum):
    PENDING = auto()
    PAYED = auto()
    PROCESSING = auto()
    SHIPPED = auto()
    DELIVERED = auto()

class OrderItems(BaseModel):
    product_id: int
    quantity: int

class OrderRequest(BaseModel):
    items: list[OrderItems]

class Order(BaseModel):
    id: str
    created_at: datetime
    items: list[OrderItems]
    status: OrderStatus
    payment_amount: float
    
class CreditCardPayment(BaseModel):
    name: str
    number: int
    valid_thru: date

class StatusResponse(BaseModel):
    status: str
