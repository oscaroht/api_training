from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/sku/")
def get_sku(product_id: int):
    """Returns the stock of a certain product"""
    return 5

@app.put("/ship")
def ship(order_id):
    return


