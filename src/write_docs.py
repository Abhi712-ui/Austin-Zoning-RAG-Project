import json
from helper_functions.walk_tree import get_content
from helper_functions.save_section import save_section
from config import (
    WRITE_DIR,
    CORPUS_DIR
)

file_path = WRITE_DIR / "leaf_nodes.json"

with open(file_path, "r", encoding="utf-8") as file:
    leaf_nodes = json.load(file)
    
test_content = get_content(
    leaf_nodes[0]["id"]
)

docs = test_content["Docs"]

for doc in docs[:10]:
    save_section(doc)
    

