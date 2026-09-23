"""Parse the section 25-2-491 use table into flat (use, district, permission) rows."""
import re
from bs4 import BeautifulSoup

PROHIBITED = {"\u2014", "X"}

CELL_RE        = re.compile(r"^(P|C|PC|CP)?(\d+)?$")
NAME_MARKER_RE = re.compile(r"^(.*?)\s+(\d{1,2})$")
CATEGORY_RE    = re.compile(r"^[A-Z]+ USES$")
NOTE_ITEM_RE   = re.compile(r"^(\d{1,2})[\s\u2013\-]+(.*)$", re.S)
LEGEND_RE      = re.compile(r"^(PC|CP)\s*[\u2013\-]\s*(.*)$", re.S)


def _cells(row):
    return [c.get_text(" ", strip=True).replace("\u2002", " ").replace("\u2003", " ").strip()
            for c in row.find_all(["td", "th"])]


def split_use_name(text):
    m = NAME_MARKER_RE.match(text)
    return (m.group(1).strip(), int(m.group(2))) if m else (text, None)


def parse_cell(raw):
    v = raw.strip()
    if v == "":
        return None, None
    if v in PROHIBITED:
        return "NOT_PERMITTED", None
    m = CELL_RE.match(v)
    if not m:
        raise ValueError(f"unrecognised cell value: {v!r}")
    letters, digits = m.group(1), m.group(2)
    note = int(digits) if digits else None
    return (letters if letters else "SEE_NOTE"), note


def parse_notes(text):
    notes, legend = {}, {}
    # notes are ";"-separated, but the PC/CP legend runs on without one
    for part in re.split(r";\s*|(?=\bPC\s*[\u2013-]\s)|(?=\bCP\s*[\u2013-]\s)", text):
        part = " ".join(part.split()).rstrip(".")
        if not part:
            continue
        m = LEGEND_RE.match(part)
        if m:
            legend[m.group(1)] = m.group(2).strip()
            continue
        m = NOTE_ITEM_RE.match(part)
        if m:
            notes[int(m.group(1))] = m.group(2).strip()
            continue
        raise ValueError(f"unrecognised notes fragment: {part!r}")
    return notes, legend


def parse_use_table(html, section_id):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("no <table> found in document")

    districts, category, rows = None, None, []
    notes, legend, skipped = {}, {}, []

    for tr in table.find_all("tr"):
        cells = _cells(tr)

        if len(cells) == 1:
            text = cells[0]
            if CATEGORY_RE.match(text):
                category = text
            elif NOTE_ITEM_RE.match(text):
                notes, legend = parse_notes(text)
            elif "=" in text or "TABLE" in text:
                skipped.append(text)
            else:
                raise ValueError(f"unexpected single-cell row: {text!r}")
            continue

        if cells[0] == "":
            if districts is not None:
                raise ValueError("second header row encountered")
            districts = cells[1:]
            continue

        if districts is None:
            raise ValueError("use row before header row")
        if len(cells) != len(districts) + 1:
            raise ValueError(f"row {cells[0]!r} has {len(cells)} cells, expected {len(districts)+1}")

        use, use_note_ref = split_use_name(cells[0])
        for district, raw in zip(districts, cells[1:]):
            permission, note_ref = parse_cell(raw)
            if permission is None:
                continue
            rows.append({
                "section_id": section_id, "category": category,
                "use": use, "use_note_ref": use_note_ref,
                "district": district, "permission": permission,
                "note_ref": note_ref, "raw": raw,
            })

    if districts is None:
        raise ValueError("no header row found")

    referenced  = {r["note_ref"] for r in rows if r["note_ref"]}
    referenced |= {r["use_note_ref"] for r in rows if r["use_note_ref"]}
    undefined = sorted(referenced - set(notes))
    if undefined:
        raise ValueError(f"note refs used but never defined: {undefined}")

    return {"districts": districts, "rows": rows, "notes": notes,
            "legend": legend, "skipped_rows": skipped}