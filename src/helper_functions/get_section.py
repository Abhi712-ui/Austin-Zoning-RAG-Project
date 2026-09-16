import json
from bs4 import BeautifulSoup
from helper_functions.walk_tree import get_content
from config import  (
    WRITE_DIR
)

file_path = WRITE_DIR / "leaf_nodes.json"
with open(file_path, "r", encoding="utf-8") as file:
    leaf_nodes = json.load(file)
    
leaf_ids = {node["id"] for node in leaf_nodes}

seen_ids = set()
all_docs = {}
request_count = 0

for node in leaf_nodes:
    if node["id"] in seen_ids: continue
    print(f"Requesting group containing: {node['heading']}")
    response = get_content(node["id"])
    request_count += 1
    for doc in response["Docs"]:
        seen_ids.add(doc["Id"])
        all_docs[doc["Id"]] = doc

content_docs = {
    doc_id: doc for doc_id, doc in all_docs.items() 
    if doc_id in leaf_ids
}

def get_section_text(title):
    for doc in content_docs.values():
        if doc["Title"] == title:
            soup = BeautifulSoup(doc["Content"], "html.parser")
            return soup.get_text()

    return None

def get_section_code(title):
    for doc in content_docs.values():
        if doc["Title"] == title:
            soup = BeautifulSoup(doc["Content"], "html.parser")
            return soup.prettify()
    return None

