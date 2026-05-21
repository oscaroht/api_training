import sqlite3

DB_FILE = 'warehouse.db'

def query(stmt: str):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        result = cursor.execute(stmt)
        connection.commit()
    return result.fetchall()

def db_init():
    stmt = """
        CREATE TABLE stock (
            product_id INT,
            stock INT
        );
    """
    query(stmt)

