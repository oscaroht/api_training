from datetime import UTC, date, datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import Order, OrderRequest, CreditCardPayment, OrderStatus
from db import db_init, insert_order
import uuid
import requests

app = FastAPI()

CATALOG_BASE_URL = 'https://127.0.0.1/'

db_init()


@app.post("/order")
def create_order(order_request: OrderRequest):
    """Uses the products in the cart to an order"""
    order_id = str(uuid.uuid4())
    total_price = 0.0
    for item in order_request.items:
        # r = requests.get(CATALOG_BASE_URL + 'product/?id=' + str(item.product_id))
        # data = r.json()
        # total_price += float(data['price']) * item.quantity
        total_price += 2 * item.quantity

    order = Order(id=order_id, created_at=datetime.now(UTC), items=order_request.items, status=OrderStatus.PENDING, payment_amount=total_price)
    insert_order(order)
    return order


@app.get("/order")
def get_order(order_id: int):
    return


def perform_payment():
    return

@app.post("/payment/")
def read_item(order_id: int, payment: CreditCardPayment):
    """Pay and decrease stock"""
    perform_payment()
    # update_status(order_id, OrderStatus.PAYED)
    # ship(order_id)
    return
