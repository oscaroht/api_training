from fastapi import FastAPI, HTTPException
from db import db_init, get_product, search_products
from models import Product

app = FastAPI()

db_init()


@app.get("/search_products", response_model=list[Product])
def search(color: str | None = None, size: str | None = None, sort_by: str = "price"):
    """Search products with different filters and different sortings. For example color and size. Used by external customers."""
    try:
        return search_products(color=color, size=size, sort_by=sort_by)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/product", response_model=Product)
def get_product_endpoint(id: int):
    """Get the product with a specific ID. Mostly used for internal use."""
    product = get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
