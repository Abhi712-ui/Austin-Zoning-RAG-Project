from bs4 import BeautifulSoup
import os
from config import (
    CORPUS_DIR
)


def save_section(section):
    heading = section["Title"]
    soup = BeautifulSoup(section["Content"], "html.parser")
    text = soup.get_text("\n", strip=True)
    if not text:
        print(f"Skipping empty doc {heading}")
        return
    file_path = os.path.join(CORPUS_DIR, f"{heading}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote Text Successfully at {file_path}")
    
def parse_section(section):
    heading = section["Title"]
    soup = BeautifulSoup(section["Content"], "html.parser")
    text = soup.get_text("\n", strip=True)
    return {
        "id": section["Id"],
        "heading": heading,
        "text": text
    }