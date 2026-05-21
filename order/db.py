import sqlite3

from models import Order

DB_FILE = 'order.db'

def query(stmt: str, params={}):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        result = cursor.execute(stmt, params)
        connection.commit()
    return result.fetchall()

def db_init():
    stmts = [
        """
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT,
            created_at DATETIME DEFAULT current_timestamp,
            status TEXT DEFAULT 'pending',
            payment_amount REAL
        );""",
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_id TEXT,
            product_id INTEGER,
            quantity INTEGER,
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
        """]
    for stmt in stmts:
        query(stmt)

def insert_order(order: Order):
    query(
        "INSERT INTO orders (id, created_at, status, payment_amount) VALUES (:id, :created_at, :status, :payment_amount)",
        order.model_dump()
    )
    for item in order.items:
        params = item.model_dump()
        params['order_id'] = order.id
        query("INSERT INTO order_items (order_id, product_id, quantity) VALUES (:order_id, :product_id, :quantity)", params)

def select_order(order_id: str):
    rows = query("""
        SELECT o.id, o.created_at, o.status, o.payment_amount, oi.product_id, oi.quantity
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        WHERE o.id = :order_id
    """, {'order_id': order_id})
    if not rows:
        return None
    id, created_at, status, payment_amount = rows[0][:4]
    items = [{'product_id': row[4], 'quantity': row[5]} for row in rows if row[4] is not None]
    return {'id': id, 'created_at': created_at, 'status': status, 'payment_amount': payment_amount, 'items': items}

def update_order_status(order_id: str, status: str):
    query("UPDATE orders SET status = :status WHERE id = :order_id", {'order_id': order_id, 'status': status})
