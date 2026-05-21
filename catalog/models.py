from pydantic import BaseModel


class Product(BaseModel):
    id: int
    description: str
    color: str
    size: str
    price: float
