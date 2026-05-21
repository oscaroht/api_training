from datetime import UTC, datetime
from fastapi import FastAPI, HTTPException
from models import Order, OrderRequest, CreditCardPayment, OrderStatus, StatusResponse
from db import db_init, insert_order, select_order, update_order_status
import uuid
import requests

app = FastAPI()

CATALOG_BASE_URL = 'http://127.0.0.1:8000'
WAREHOUSE_BASE_URL = 'http://127.0.0.1:8002'

db_init()


@app.post("/order", response_model=Order)
def create_order(order_request: OrderRequest):
    """User initiates order"""
    order_id = str(uuid.uuid4())
    total_price = 0.0
    for item in order_request.items:
        r = requests.get(CATALOG_BASE_URL + '/product', params={'id': item.product_id})
        r.raise_for_status()
        total_price += float(r.json()['price']) * item.quantity

    order = Order(id=order_id, created_at=datetime.now(UTC), items=order_request.items,
                  status=OrderStatus.PENDING, payment_amount=total_price)
    insert_order(order)
    return order


@app.get("/order", response_model=Order)
def get_order(order_id: str):
    """User or other microservices can get an order by id"""
    order = select_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/order_status", response_model=StatusResponse)
def update_status(order_id: str, status: OrderStatus):
    """Allows other microservices to alter the status."""
    update_order_status(order_id, status)
    return StatusResponse(status=status)


@app.post("/payment/", response_model=StatusResponse)
def pay(order_id: str, payment: CreditCardPayment):
    """Pay and decrease stock in the warehouse"""
    order = select_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_order_status(order_id, OrderStatus.PAYED)

    for item in order['items']:
        requests.put(WAREHOUSE_BASE_URL + '/decrease_stock',
                     params={'product_id': item['product_id'], 'quantity': item['quantity']})

    requests.put(WAREHOUSE_BASE_URL + '/ship', params={'order_id': order_id})
    return StatusResponse(status="payed")
