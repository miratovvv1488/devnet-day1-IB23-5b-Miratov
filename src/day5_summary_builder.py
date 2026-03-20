#!/usr/bin/env python3
import hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

ART = Path("artifacts/day5")
SCHEMA_VERSION = "5.0"

def now_utc(): return datetime.now(timezone.utc).isoformat()
def sha256_text(s: str): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def sha256_file(p: Path) -> str:
    if not p.exists(): return ""
    return sha256_text(p.read_text(encoding="utf-8", errors="replace"))

def token_hash8(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

def contains(p: Path, needle: str) -> bool:
    return needle in read(p)

def main() -> int:
    token = os.getenv("STUDENT_TOKEN", "").strip()
    name = os.getenv("STUDENT_NAME", "").strip()
    group = os.getenv("STUDENT_GROUP", "").strip()
    th8 = token_hash8(token) if token else ""

    yang_ok = contains(ART/"yang"/"pyang_tree.txt", "+--rw interfaces")
    webex_ok = contains(ART/"webex"/"room_create.json", th8)
    pt_ok = contains(ART/"pt"/"external_access_check.json", "empty ticket")
    net_ok = contains(ART/"pt"/"network_devices.json", "1.0")
    hosts_ok = contains(ART/"pt"/"hosts.json", "1.0")

    summary = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": now_utc(),
        "student": {"token": token, "token_hash8": th8, "name": name, "group": group},
        "yang": {"ok": yang_ok, "evidence_sha": sha256_file(ART/"yang"/"pyang_tree.txt")},
        "webex": {"ok": webex_ok, "room_title_contains_hash8": webex_ok, "evidence_sha": sha256_file(ART/"webex"/"room_create.json")},
        "pt": {"ok": pt_ok and net_ok and hosts_ok, "empty_ticket_seen": pt_ok, "evidence_sha": sha256_file(ART/"pt"/"external_access_check.json")},
        "validation_passed": bool(yang_ok and webex_ok and pt_ok),
        "run": {"python": sys.version.split()[0], "platform": sys.platform},
    }

    out = ART / "summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["validation_passed"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
