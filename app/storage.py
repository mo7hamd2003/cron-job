# app/storage.py
import json
from pathlib import Path

STORAGE_DIR = Path(__file__).resolve().parent.parent / "dictionary"
STORAGE_DIR.mkdir(exist_ok=True)

def save_report(record: dict) -> None:
    (STORAGE_DIR / f"{record['id']}.json").write_text(json.dumps(record))

def load_report(report_id: str) -> dict:
    return json.loads((STORAGE_DIR / f"{report_id}.json").read_text())

def load_all_reports() -> list[dict]:
    return [json.loads(f.read_text()) for f in STORAGE_DIR.glob("*.json")]