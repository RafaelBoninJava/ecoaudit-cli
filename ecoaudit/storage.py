import json
import os
from typing import Any, Dict, List

AUDITS_DIR = os.path.join("data", "audits")


def ensure_dirs() -> None:
    os.makedirs(AUDITS_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)


def save_audit_json(audit: Dict[str, Any], audit_id: str) -> str:
    ensure_dirs()
    path = os.path.join(AUDITS_DIR, f"audit_{audit_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=4, ensure_ascii=False)
    return path


def list_audit_files() -> List[str]:
    if not os.path.isdir(AUDITS_DIR):
        return []
    files = [f for f in os.listdir(AUDITS_DIR) if f.startswith("audit_") and f.endswith(".json")]
    files.sort(reverse=True)
    return files


def load_audit_json(filename: str) -> Dict[str, Any]:
    path = os.path.join(AUDITS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)