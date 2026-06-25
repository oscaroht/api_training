from fastapi import FastAPI
from db import db_init

app = FastAPI()

CATALOG_BASE_URL = 'http://127.0.0.1:8000'
WAREHOUSE_BASE_URL = 'http://127.0.0.1:8002'

db_init()


@app.get("/")
def root():
    return {'message': 'hello world'}
