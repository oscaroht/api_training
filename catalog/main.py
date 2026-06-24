import requests
from fastapi import FastAPI, HTTPException
from db import db_init, get_product, search_products
from models import Product, ProductDetail

app = FastAPI()

WAREHOUSE_BASE_URL = 'http://127.0.0.1:8002'

db_init()


@app.get("/products", response_model=list[Product])
def search(color: str | None = None, size: str | None = None, sort_by: str = "price"):
    """Search products with different filters and different sortings. For example color and size. Used by external customers."""
    try:
        return search_products(color=color, size=size, sort_by=sort_by)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/products/{id}", response_model=ProductDetail)
def get_product_endpoint(id: int):
    """Get the product with a specific ID, including its current stock. Mostly used for internal use."""
    product = get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        r = requests.get(f"{WAREHOUSE_BASE_URL}/products/{id}/stock", timeout=5)
        r.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Could not retrieve stock from warehouse")

    return ProductDetail(**product, stock=r.json()["stock"])
