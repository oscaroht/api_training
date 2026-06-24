import requests
from fastapi import FastAPI, HTTPException
from db import db_init, get_stock, decrease_stock
from models import StockResponse, StatusResponse, StockUpdate, ShipmentRequest

app = FastAPI()

ORDER_BASE_URL = 'http://127.0.0.1:8001'

db_init()


@app.get("/products/{product_id}/stock", response_model=StockResponse)
def get_sku(product_id: int):
    """Looks up the stock of a certain product from the database and returns the amount"""
    return StockResponse(product_id=product_id, stock=get_stock(product_id))


@app.patch("/products/{product_id}/stock", response_model=StatusResponse)
def decrease(product_id: int, update: StockUpdate):
    """Decreases stock after a successful payment"""
    if get_stock(product_id) < update.quantity:
        raise HTTPException(status_code=409, detail="Insufficient stock")
    decrease_stock(product_id, update.quantity)
    return StatusResponse(status="ok")


@app.post("/shipments", response_model=StatusResponse)
def ship(shipment: ShipmentRequest):
    """Ships the order and updates the order status to shipped"""
    requests.patch(ORDER_BASE_URL + f"/orders/{shipment.order_id}", json={"status": "shipped"})
    return StatusResponse(status="shipped")
