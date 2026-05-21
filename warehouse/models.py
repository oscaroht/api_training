from pydantic import BaseModel


class StockResponse(BaseModel):
    product_id: int
    stock: int


class StatusResponse(BaseModel):
    status: str
