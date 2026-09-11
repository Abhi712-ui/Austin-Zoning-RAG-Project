import json
from config import WRITE_DIR

file_path = WRITE_DIR / "products.json"
with open(file_path, "r", encoding="utf-8") as file:
    products = json.load(file)

land_development = next(
    product for product in products["codes"]
    if product["productName"].lower() == "land development code"
)

product_id = land_development["productId"]
print(json.dumps(product_id, indent=4))
print(f"Product Id: {product_id}")