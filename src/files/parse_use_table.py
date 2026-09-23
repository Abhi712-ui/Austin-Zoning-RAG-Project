import json
from helper_functions.use_table import parse_use_table
from config import RAW_DIR, PARSED_DIR, USE_TABLE_ID, JOB_ID

html = (RAW_DIR / f"{USE_TABLE_ID}.html").read_text(encoding="utf-8")
result = parse_use_table(html, USE_TABLE_ID)
PARSED_DIR.mkdir(parents=True, exist_ok=True)

out = {
    "job_id": JOB_ID,
    "section_id": USE_TABLE_ID,
    "districts": result["districts"],
    "notes": result["notes"],
    "legend": result["legend"],
    "rows": result["rows"],
}

with open(PARSED_DIR / "zoning_uses.json", "w", encoding="utf-8") as file:
    json.dump(out, file, indent=2)

rows = result["rows"]

print(
    f"{len(result['districts'])} districts | "
    f"{len({r['use'] for r in rows})} uses | "
    f"{len(rows)} rows | {len(result['notes'])} notes"
)