import json
import requests
from config import (
    API, 
    CLIENT_ID, 
    WRITE_DIR, 
    PRODUCT_ID, 
    JOB_ID, 
    TITLE_25_ID,
    ZONING_SECTION_ID 
)
from pathlib import Path

#helper function
def get_api(path, params=None):
    response = requests.get(
        f"{API}/{path}",
        params=params
    )
    response.raise_for_status()
    return response.json()

#client information
path = f"/Clients/{CLIENT_ID}"
client = get_api(path)
WRITE_DIR.mkdir(parents=True, exist_ok=True)
output_file = WRITE_DIR / "client.json"
with open(output_file, "w") as file:
    json.dump(client, file, indent=4)
    
#get client content
path = f"/ClientContent/{CLIENT_ID}"
products = get_api(path)
WRITE_DIR.mkdir(parents=True, exist_ok=True)
output_file = WRITE_DIR / "products.json"
with open(output_file, "w") as file:
    json.dump(products, file, indent=4)

#get information on the current version
path = f"/Jobs/latest/{PRODUCT_ID}"
current_version = get_api(path)
WRITE_DIR.mkdir(parents=True, exist_ok=True)
output_file = WRITE_DIR / "current_version.json"
with open(output_file, "w") as file:
    json.dump(current_version, file, indent=4)

#get table of contents
path = f"/codesToc"
params = {
    "jobId": JOB_ID,
    "productId": PRODUCT_ID
}
get_toc = get_api(path, params)
WRITE_DIR.mkdir(parents=True, exist_ok=True)
output_file = WRITE_DIR / "get_toc.json"
with open(output_file, "w") as file:
    json.dump(get_toc, file, indent=4)

#get children for title 25 from the table of contents
path = f"/codesToc/children"
params = {
    "jobId": JOB_ID,
    "nodeId": TITLE_25_ID,
    "productId": PRODUCT_ID
}
title_25_children = get_api(path, params)
WRITE_DIR.mkdir(parents=True, exist_ok=True)
output_file = WRITE_DIR / "title_25_children.json"
with open(output_file, "w") as file:
    json.dump(title_25_children, file, indent=4)
    
#get the children for the table of contents
path = f"/codesToc/children"
params = {
    "jobId": JOB_ID,
    "nodeId": ZONING_SECTION_ID,
    "productId": PRODUCT_ID
}
zoning_children = get_api(path, params)
WRITE_DIR.mkdir(parents=True, exist_ok=True)
output_file = WRITE_DIR / "zoning_children.json"
with open(output_file, "w") as file:
    json.dump(zoning_children, file, indent=4)
    
