import sqlite3
import csv
from pathlib import Path

DB_FILE = 'catalog.db'
DATA_FILE = Path(__file__).parent.parent / 'data.csv'

ALLOWED_SORT_COLUMNS = {"price", "description", "color", "size", "id"}


def query(stmt: str, params={}):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        result = cursor.execute(stmt, params)
        connection.commit()
    return result.fetchall()

def db_init():
    query("""
        CREATE TABLE IF NOT EXISTS product (
            id INT PRIMARY KEY,
            description TEXT,
            color TEXT,
            size TEXT,
            price DECIMAL
        );
    """)
    if query("SELECT COUNT(*) FROM product")[0][0] == 0:
        with open(DATA_FILE) as f:
            rows = [r for r in csv.DictReader(f)]
        for row in rows:
            query(
                "INSERT INTO product (id, description, color, size, price) VALUES (:id, :description, :color, :size, :price)",
                row
            )

def get_product(id: int):
    rows = query("SELECT id, description, color, size, price FROM product WHERE id = :id", {'id': id})
    if not rows:
        return None
    id, description, color, size, price = rows[0]
    return {'id': id, 'description': description, 'color': color, 'size': size, 'price': price}

def search_products(color=None, size=None, sort_by="price"):
    if sort_by not in ALLOWED_SORT_COLUMNS:
        raise ValueError(f"Invalid sort column: {sort_by}")
    rows = query(f"""
        SELECT id, description, color, size, price FROM product
        WHERE 1=1
        AND (:color IS NULL OR color = :color)
        AND (:size IS NULL OR size = :size)
        ORDER BY {sort_by}
    """, {'color': color, 'size': size})
    return [{'id': r[0], 'description': r[1], 'color': r[2], 'size': r[3], 'price': r[4]} for r in rows]
