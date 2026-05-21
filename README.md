# E-commerce Microservices — FastAPI Training

A training project for data engineers learning FastAPI. The system is split into three independent microservices that communicate over HTTP.

## Services

| Service   | Port | Responsibility                        |
|-----------|------|---------------------------------------|
| Catalog   | 8000 | Product information and search        |
| Order     | 8001 | Order lifecycle and payment           |
| Warehouse | 8002 | Stock levels and shipping             |

## Order Flow

```
Customer
   │
   ├─1─▶ GET  /search_products        (Catalog)   Browse products
   ├─2─▶ GET  /product?id=            (Catalog)   Get product details + price
   │
   ├─3─▶ POST /order                  (Order)     Place order
   │          └─▶ GET /product?id=    (Catalog)   Fetch price per item
   │
   ├─4─▶ POST /payment/               (Order)     Pay for order
   │          ├─▶ PUT /decrease_stock (Warehouse) Decrease stock per item
   │          └─▶ PUT /ship           (Warehouse) Trigger shipment
   │                   └─▶ PUT /order_status      (Order) Set status → shipped
   │
   └─5─▶ GET  /order?order_id=        (Order)     Check order status
```

## Endpoints

### Catalog — port 8000

| Method | Path               | Description                                      |
|--------|--------------------|--------------------------------------------------|
| GET    | `/product`         | Get a single product by `id`                     |
| GET    | `/search_products` | Search by `color`, `size`; sort with `sort_by`   |

### Order — port 8001

| Method | Path             | Description                                      |
|--------|------------------|--------------------------------------------------|
| POST   | `/order`         | Place a new order; fetches prices from Catalog   |
| GET    | `/order`         | Get order by `order_id`                          |
| PUT    | `/order_status`  | Update order status (used by Warehouse)          |
| POST   | `/payment/`      | Pay for an order; triggers stock decrease + ship |

### Warehouse — port 8002

| Method | Path               | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/sku/`            | Get current stock for a `product_id` |
| PUT    | `/decrease_stock`  | Decrease stock after payment         |
| PUT    | `/ship`            | Ship order and notify Order service  |

## Test Data

Product and stock data lives in `data.csv` at the project root. Both the Catalog and Warehouse services load it automatically on first startup — if the database is empty, all rows from the CSV are inserted. Restarting the service will not duplicate the data.

To reset to the original data, delete the database files and restart:

```bash
rm catalog/catalog.db warehouse/warehouse.db
```

## Database Tables

| Service   | Table         | Columns                                              |
|-----------|---------------|------------------------------------------------------|
| Catalog   | `product`     | id, description, color, size, price                  |
| Order     | `orders`      | id, created_at, status, payment_amount               |
| Order     | `order_items` | order_id, product_id, quantity                       |
| Warehouse | `stock`       | product_id, stock                                    |

## Running the Services

Each service runs on a separate machine on the same network. Before starting, collect the IP address of each machine and share them with the group.

**Find your IP address:**
```bash
# Linux/Mac
hostname -I

# Windows
ipconfig
```

Once all IPs are known, update the base URLs in the service that makes outgoing calls:

| File            | Variable            | Set to                        |
|-----------------|---------------------|-------------------------------|
| `order/main.py` | `CATALOG_BASE_URL`  | `http://<catalog-machine-ip>:8000` |
| `order/main.py` | `WAREHOUSE_BASE_URL`| `http://<warehouse-machine-ip>:8002` |
| `warehouse/main.py` | `ORDER_BASE_URL`| `http://<order-machine-ip>:8001` |

Then start your assigned service, binding to `0.0.0.0` so it accepts connections from other machines on the network:

```bash
# Catalog machine
cd catalog && uvicorn main:app --host 0.0.0.0 --port 8000

# Order machine
cd order && uvicorn main:app --host 0.0.0.0 --port 8001

# Warehouse machine
cd warehouse && uvicorn main:app --host 0.0.0.0 --port 8002
```

Each service exposes interactive API docs at `http://<machine-ip>:<port>/docs`.

## Order Status Lifecycle

```
PENDING → PAYED → SHIPPED
```
