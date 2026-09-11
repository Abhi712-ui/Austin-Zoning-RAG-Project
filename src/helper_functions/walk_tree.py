from config import (
    JOB_ID,
    PRODUCT_ID,
)
from municode import get_api

#get the children for a particular node
def get_children(node_id):
    path = f"/codesToc/children"
    params = {
        "jobId": JOB_ID,
        "nodeId": node_id,
        "productId": PRODUCT_ID
    }
    return get_api(path, params)

#traverse nested documents
def walk_tree(node, hierarchy=None):
    if hierarchy is None:
        hierarchy = []

    current_hierarchy = hierarchy + [node["Heading"]]

    nodes = [{
        "id": node["Id"],
        "heading": node["Heading"],
        "node_depth": node["NodeDepth"],
        "parent_id": node["ParentId"],
        "has_children": node["HasChildren"],
        "doc_order_id": node["DocOrderId"],
        "hierarchy": current_hierarchy
    }]

    if node["HasChildren"]:
        children = get_children(node["Id"])
        for child in children:
            nodes.extend(
                walk_tree(
                    child,
                    current_hierarchy
                )
            )
    return nodes

#get the content of a node
def get_content(node_id):
    print(f"Fetching children of: {node_id}")
    path = f"/CodesContent"
    params={
            "jobId": JOB_ID,
            "nodeId": node_id,
            "productId": PRODUCT_ID
        }
    return get_api(path, params)