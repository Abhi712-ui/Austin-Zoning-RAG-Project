from pathlib import Path
import json
import requests
import parsing_help

API = "https://api.municode.com"
STATE = "TX"
CLIENT = "Austin"
CLIENT_ID = "1113"
PRODUCT_ID = 15303
JOB_ID = 488379
TITLE_25_ID = "TIT25LADE"
ZONING_SECTION_ID = "TIT25LADE_CH25-2ZO"

get_table_of_contents = requests.get(
    f"{API}/codesToc",
    params={
        "jobId": JOB_ID,
        "productId": PRODUCT_ID
    }
)
get_table_of_contents.raise_for_status()
toc = get_table_of_contents.json()

Path("data/raw").mkdir(parents=True, exist_ok=True)
with open("data/raw/toc.json", "w") as f:
    json.dump(toc, f, indent=4)
    

    
chapter_matches = parsing_help.find_nodes(toc, "CHAPTER 25-2")
#for match in chapter_matches:
    #print(json.dumps(match, indent=4))
    


response = requests.get(
    f"{API}/codesToc/children",
    params={
        "jobId": JOB_ID,
        "nodeId": TITLE_25_ID,
        "productId": PRODUCT_ID
    }
)

response.raise_for_status()
title_25_children = response.json()

Path("data/raw").mkdir(parents=True, exist_ok=True)
with open("data/raw/title25.json", "w") as f:
    json.dump(title_25_children, f, indent=4)
    
response = requests.get(
    f"{API}/codesToc/children",
    params={
        "jobId": JOB_ID,
        "nodeId": ZONING_SECTION_ID,
        "productId": PRODUCT_ID
    }
)

response.raise_for_status()
zoning_children = response.json()

with open("data/raw/zoningchildren.json", "w") as f:
    json.dump(zoning_children, f, indent=4)
    
all_zoning_nodes = []

for child in zoning_children:
    all_zoning_nodes.extend(
        parsing_help.walk_tree(
            child,
            hierarchy=["CHAPTER 25-2. ZONING"]
        )
    )

print("Total zoning nodes:", len(all_zoning_nodes))

with open("data/raw/zoning_nodes.json", "w") as f:
    json.dump(all_zoning_nodes, f, indent=4)
    
leaf_nodes = [
    node for node in all_zoning_nodes
    if not node["has_children"]
]

print(json.dumps(leaf_nodes[0], indent=4))

test_content = parsing_help.get_content(
    leaf_nodes[0]["id"]
)

print(json.dumps(test_content, indent=4))