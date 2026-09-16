from pathlib import Path

API = "https://api.municode.com"
STATE = "TX"
CLIENT = "Austin"
CLIENT_ID = "1113"
PRODUCT_ID = 15303
JOB_ID = 497334
TITLE_25_ID = "TIT25LADE"
ZONING_SECTION_ID = "TIT25LADE_CH25-2ZO"
CHUNK_THRESHOLD = 5000
ROOT = Path(__file__).resolve().parent.parent
WRITE_DIR = ROOT / "data"
CORPUS_DIR = ROOT / "corpus"
RAW_DIR = WRITE_DIR / "raw" / str(JOB_ID)