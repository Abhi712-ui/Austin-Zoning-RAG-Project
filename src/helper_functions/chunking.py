from bs4 import BeautifulSoup

def split_incr1(record, doc):
    soup = BeautifulSoup(doc["Content"], "html.parser")
    content = soup.find("div", class_="chunk-content")

    chunks = []
    current_parts = []
    current_marker = None
    chunk_number = 0

    for element in content.find_all(recursive=False):
        classes = element.get("class", [])
        # Don't include ordinance history in retrieval text
        if "historynote0" in classes: continue

        # Beginning of a new top-level definition
        if "incr1" in classes:

            # Save previous chunk
            if current_marker is not None:
                chunks.append({
                    "chunk_id": f"{record['id']}::definition::{chunk_number}",
                    "section_id": record["id"],
                    "section_heading": record["heading"],
                    "chunk_heading": current_marker,
                    "hierarchy": record["hierarchy"],
                    "text": "\n".join(current_parts)
                })

                chunk_number += 1

            current_marker = element.get_text(" ", strip=True)

            current_parts = [record["heading"], current_marker]

        # Once a definition has started, everything belongs to it
        # until the next incr1
        elif current_marker is not None:
            text = element.get_text("\n", strip=True)
            if text: current_parts.append(text)

    # Don't forget the final definition
    if current_marker is not None:
        chunks.append({
            "chunk_id": f"{record['id']}::definition::{chunk_number}",
            "section_id": record["id"],
            "section_heading": record["heading"],
            "chunk_heading": current_marker,
            "hierarchy": record["hierarchy"],
            "text": "\n".join(current_parts)
        })

    return chunks

def whole_section_chunk(record):
    return {
        "chunk_id": f"{record['id']}::0",
        "section_id": record["id"],
        "section_heading": record["heading"],
        "chunk_heading": record["heading"],
        "hierarchy": record["hierarchy"],
        "text": record["text"]
    }

def make_chunk(
    record, 
    text,
    chunk_heading,
    chunk_number,
    chunk_type
):
    return {
        "chunk_id": (
            f"{record['id']}::{chunk_type}::{chunk_number}"
        ),
        "section_id": record["id"],
        "section_heading": record["heading"],
        "chunk_heading": chunk_heading,
        "hierarchy": record["hierarchy"],
        "text": text
    }


def get_chunk_content(doc):
    soup = BeautifulSoup(doc["Content"], "html.parser")

    return soup.find("div", class_="chunk-content")

