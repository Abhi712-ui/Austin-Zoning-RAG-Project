import json
from helper_functions.walk_tree import walk_tree, get_content
from config import (
    WRITE_DIR,
    CORPUS_DIR
)

file_path = WRITE_DIR / "zoning_children.json"
with open(file_path, "r", encoding="utf-8") as file:
    zoning_children = json.load(file)

all_zoning_nodes = []
for child in zoning_children:
    all_zoning_nodes.extend(
        walk_tree(child, hierarchy=["CHAPTER 25-2. ZONING"])
    )

print("Total zoning nodes:", len(all_zoning_nodes))
WRITE_DIR.mkdir(parents=True, exist_ok=True)
output_file = WRITE_DIR / "all_zoning_nodes.json"
with open(output_file, "w") as file:
    json.dump(all_zoning_nodes, file, indent=4)
    
#grab the leaf nodes
leaf_nodes = [
    node for node in all_zoning_nodes
    if not node["has_children"]
]

file_path = WRITE_DIR / "leaf_nodes.json"
with open(file_path, "w") as file:
    json.dump(leaf_nodes, file, indent=4)
    
#try getting the content from one of the leaf nodes
test_content = get_content(
    leaf_nodes[0]["id"]
)

docs = test_content["Docs"]
CORPUS_DIR.mkdir(parents=True, exist_ok=True)
file_path = CORPUS_DIR / "test_documents.txt"

with open(file_path, "w") as file:
    for i, doc in enumerate(docs, start=1):
        file.write(f"{i}. {doc['Id']} -> {doc['Title']}\n")