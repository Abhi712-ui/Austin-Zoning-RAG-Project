import argparse
from pathlib import Path
import json
import requests


API = "https://api.municode.com"
STATE = "TX"
CLIENT = "Austin"
CLIENT_ID = "1113"
PRODUCT_ID = 15303
JOB_ID = 488379

response = requests.get(
    f"{API}/Clients/{CLIENT_ID}"
)

response.raise_for_status()
client = response.json()
print(json.dumps(client, indent=4))

products = requests.get(
    f"{API}/ClientContent/{CLIENT_ID}"
).json()

#print(type(products))
#print(json.dumps(products, indent=4))

land_development = next(
    product for product in products["codes"] if product["productName"].lower() == "land development code"
)

product_id = land_development["productId"]
print(json.dumps(land_development, indent=4))
print("Product ID:", product_id)

response = requests.get(
    f"{API}/Jobs/latest/{PRODUCT_ID}"
)

response.raise_for_status()
current_version = response.json()
print(json.dumps(current_version, indent=4))

get_table_of_contents = requests.get(
    f"{API}/codesToc",
    params={
        "job id": JOB_ID,
        "product id": PRODUCT_ID
    }
)

get_table_of_contents.raise_for_status()
toc = get_table_of_contents.json()

print(json.dumps(toc, indent=4))