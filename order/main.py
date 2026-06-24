from datetime import UTC, datetime
from fastapi import FastAPI, HTTPException
from models import Order, OrderRequest, CreditCardPayment, OrderStatus, StatusResponse, StatusUpdate
from db import db_init, insert_order, select_order, update_order_status
import uuid
import requests

app = FastAPI()

CATALOG_BASE_URL = 'http://127.0.0.1:8000'
WAREHOUSE_BASE_URL = 'http://127.0.0.1:8002'

db_init()


@app.post("/orders", response_model=Order)
def create_order(order_request: OrderRequest):
    """User initiates order"""
    order_id = str(uuid.uuid4())
    total_price = 0.0
    for item in order_request.items:
        r = requests.get(CATALOG_BASE_URL + f'/products/{item.product_id}')
        r.raise_for_status()
        total_price += float(r.json()['price']) * item.quantity

    order = Order(id=order_id, created_at=datetime.now(UTC), items=order_request.items,
                  status=OrderStatus.PENDING, payment_amount=total_price)
    insert_order(order)
    return order


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    """User or other microservices can get an order by id"""
    order = select_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.patch("/orders/{order_id}", response_model=StatusResponse)
def update_status(order_id: str, update: StatusUpdate):
    """Allows other microservices to alter the status."""
    update_order_status(order_id, update.status)
    return StatusResponse(status=update.status)


@app.post("/orders/{order_id}/payment", response_model=StatusResponse)
def pay(order_id: str, payment: CreditCardPayment):
    """Pay and decrease stock in the warehouse"""
    order = select_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_order_status(order_id, OrderStatus.PAYED)

    for item in order['items']:
        requests.patch(WAREHOUSE_BASE_URL + f"/products/{item['product_id']}/stock",
                       json={'quantity': item['quantity']})

    requests.post(WAREHOUSE_BASE_URL + '/shipments', json={'order_id': order_id})
    return StatusResponse(status="payed")
