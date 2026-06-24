from pydantic import BaseModel


class StockResponse(BaseModel):
    product_id: int
    stock: int


class StockUpdate(BaseModel):
    quantity: int


class ShipmentRequest(BaseModel):
    order_id: str


class StatusResponse(BaseModel):
    status: str
