import requests
from fastapi import FastAPI, HTTPException
from db import db_init, get_stock, decrease_stock
from models import StockResponse, StatusResponse

app = FastAPI()

ORDER_BASE_URL = 'http://127.0.0.1:8001'

db_init()


@app.get("/sku/", response_model=StockResponse)
def get_sku(product_id: int):
    """Looks up the stock of a certain product from the database and returns the amount"""
    return StockResponse(product_id=product_id, stock=get_stock(product_id))


@app.put("/decrease_stock", response_model=StatusResponse)
def decrease(product_id: int, quantity: int):
    """Decreases stock after a successful payment"""
    if get_stock(product_id) < quantity:
        raise HTTPException(status_code=409, detail="Insufficient stock")
    decrease_stock(product_id, quantity)
    return StatusResponse(status="ok")


@app.put("/ship", response_model=StatusResponse)
def ship(order_id: str):
    """Ships the order and updates the order status to shipped"""
    requests.put(ORDER_BASE_URL + "/order_status", params={"order_id": order_id, "status": "shipped"})
    return StatusResponse(status="shipped")
