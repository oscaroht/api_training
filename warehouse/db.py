import sqlite3
import csv
from pathlib import Path

DB_FILE = 'warehouse.db'
DATA_FILE = Path(__file__).parent.parent / 'data.csv'


def query(stmt: str, params={}):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        result = cursor.execute(stmt, params)
        connection.commit()
    return result.fetchall()

def db_init():
    query("""
        CREATE TABLE IF NOT EXISTS stock (
            product_id INT PRIMARY KEY,
            stock INT
        );
    """)
    if query("SELECT COUNT(*) FROM stock")[0][0] == 0:
        with open(DATA_FILE) as f:
            rows = [r for r in csv.DictReader(f)]
        for row in rows:
            query(
                "INSERT INTO stock (product_id, stock) VALUES (:id, :stock)",
                row
            )

def get_stock(product_id: int) -> int:
    rows = query("SELECT stock FROM stock WHERE product_id = :id", {'id': product_id})
    return rows[0][0] if rows else 0

def decrease_stock(product_id: int, quantity: int):
    query("UPDATE stock SET stock = stock - :qty WHERE product_id = :id",
          {'id': product_id, 'qty': quantity})
