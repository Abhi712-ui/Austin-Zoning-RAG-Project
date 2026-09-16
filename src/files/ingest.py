from datetime import datetime, timezone
import time
import json
from helper_functions.walk_tree import get_content
from config import  WRITE_DIR, RAW_DIR, JOB_ID, PRODUCT_ID


file_path = WRITE_DIR / "leaf_nodes.json"
with open(file_path, "r", encoding="utf-8") as file:
    leaf_nodes = json.load(file)
    
leaf_ids = {node["id"] for node in leaf_nodes}
seen_ids = set()
request_count = 0
RAW_DIR.mkdir(parents=True, exist_ok=True)

for node in leaf_nodes:
    if node["id"] in seen_ids: continue
    if (RAW_DIR / f"{node['id']}.html").exists(): continue
    print(f"Requesting group containing: {node['heading']}")
    try:
        response = get_content(node["id"])
    except Exception as e:
        print(f"FAILED {node['id']}: {e}")
        continue
    finally:
        time.sleep(0.25)
    request_count += 1
    for doc in response["Docs"]:
        seen_ids.add(doc["Id"])
        content = doc.get("Content") or ""
        (RAW_DIR / f"{doc['Id']}.html").write_text(content, encoding="utf-8")
        
with open(WRITE_DIR / "current_version.json", encoding="utf-8") as file:
    version = json.load(file)
    
written = {p.stem for p in RAW_DIR.glob("*.html")}

manifest = {
    "job_id": JOB_ID,
    "product_id": PRODUCT_ID,
    "supplement": version["Name"],
    "publish_date": version["PublishDate"],
    "fetched_at": datetime.now(timezone.utc).isoformat(),
    "leaf_node_count": len(leaf_ids),
    "docs_written": len(written),
    "request_count": request_count,
    "missing_ids": sorted(leaf_ids - written),
    "files": sorted(written),
}

with open(RAW_DIR / "manifest.json", "w", encoding="utf-8") as file:
    json.dump(manifest, file, indent=4)

print(f"{request_count} requests | {len(written)} docs | {len(manifest['missing_ids'])} missing")