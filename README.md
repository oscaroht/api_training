

Order flow:
-catalog search 
    - finds a product
    - calls warehouse to get stock level
-order add_to_shopping_cart takes a product_id
    - adds it to the shopping cart table
    - calls warehouse api to reverve the product

-order post creates a order object with status
    - create order object
-order pay 
    - changes the order object to payed 
    - calls the warehouse api to change reserves status to bought

-warehouse fulfil decreases the stock and ships the contents of the shopping cart

Endpoints:
-catalog: search
-order: add_to_cart, place_order, pay
-warehouse: get_stock, reserve_item, decrease_stock

Tables:
catalog: product_catalog
order: cart, order
warehouse: sku, ship
