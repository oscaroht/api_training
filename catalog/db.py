import sqlite3

DB_FILE = 'catalog.db'


def query(stmt: str):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        result = cursor.execute(stmt)
        connection.commit()
    return result.fetchall()

def db_init():
    stmt = """
        CREATE TABLE product (
            id INT,
            description TEXT,
            color TEXT,
            size TEXT,
            price DECIMAL
        );

    """
    query(stmt)

