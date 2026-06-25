from fastapi import FastAPI
from db import db_init

app = FastAPI()

ORDER_BASE_URL = 'http://127.0.0.1:8001'

db_init()


@app.get('/')
async def root():
    return {'message': 'hello world'}
