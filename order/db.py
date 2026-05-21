import sqlite3

from models import OrderRequest, Order

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
    print("DB initialized")

def insert_order(order: Order):
    stmt = """INSERT INTO orders (id, created_at, status, payment_amount) VALUES (:id, :created_at, :status, :payment_amount)"""
    print(stmt)
    query(stmt, order.model_dump())
    for item in order.items:
        print(item.model_dump())
        stmt = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (:id, :product_id, :quantity)"
        print(stmt)
        query(stmt, item.model_dump().update({'id': order.id}))

def select_order(order_id: int):
    raise NotImplementedError("")
