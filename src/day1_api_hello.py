#!/usr/bin/env python3
import argparse, hashlib, json, os, sys
from datetime import datetime, timezone
import requests

API_URL_DEFAULT = "https://jsonplaceholder.typicode.com/todos/1"
ART_DIR = "artifacts/day1"
RESPONSE_PATH = f"{ART_DIR}/response.json"
SUMMARY_PATH  = f"{ART_DIR}/summary.json"
LOG_PATH       = f"{ART_DIR}/run.log"

EXPECTED = {"userId": 1, "id": 1, "title": "delectus aut autem", "completed": False}
SUMMARY_SCHEMA_VERSION = "1.0"

def log(msg):
    os.makedirs(ART_DIR, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()}Z {msg}\n")

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def dump_json(obj, path):
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return text

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_payload(payload):
    errors = []
    for k, v in EXPECTED.items():
        if k not in payload:
            errors.append(f"missing_key:{k}")
        elif payload[k] != v:
            errors.append(f"bad_value:{k}:{payload[k]}!=expected")
    return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=API_URL_DEFAULT)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    os.makedirs(ART_DIR, exist_ok=True)

    token  = os.getenv("STUDENT_TOKEN", "").strip()
    name   = os.getenv("STUDENT_NAME", "").strip()
    group  = os.getenv("STUDENT_GROUP", "").strip()

    if not token or not name or not group:
        print("ERROR: set STUDENT_TOKEN, STUDENT_NAME, STUDENT_GROUP", file=sys.stderr)
        return 3

    try:
        if args.offline:
            payload = load_json(RESPONSE_PATH)
            status_code = 200
            log("OFFLINE: loaded cached response.json")
        else:
            log(f"ONLINE: GET {args.url}")
            r = requests.get(args.url, timeout=10)
            status_code = r.status_code
            payload = r.json()
            dump_json(payload, RESPONSE_PATH)

        ok, errors = validate_payload(payload)

        with open(RESPONSE_PATH, "r", encoding="utf-8") as f:
            resp_sha = sha256_text(f.read())

        summary = {
            "schema_version": SUMMARY_SCHEMA_VERSION,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "student": {"token": token, "name": name, "group": group},
            "api": {
                "url": args.url,
                "status_code": status_code,
                "validation_passed": ok and status_code == 200,
                "validation_errors": errors if status_code == 200 else ["http_status_not_200"],
                "response_sha256": resp_sha,
            },
            "run": {"python": sys.version.split()[0], "platform": sys.platform},
        }
        dump_json(summary, SUMMARY_PATH)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        log(f"DONE status={status_code} validation={summary['api']['validation_passed']}")
        return 0 if summary["api"]["validation_passed"] else 2

    except Exception as e:
        log(f"ERROR {type(e).__name__}: {e}")
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())