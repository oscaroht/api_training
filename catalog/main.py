from fastapi import FastAPI

app = FastAPI()



@app.get("/search_products")
def search():
    """Search products with different filters and different sortings"""
    return {"Hello": "World"}

@app.get("/product")
def get_product(id: int):
    return {'id': 1, 'price': 5.45}
