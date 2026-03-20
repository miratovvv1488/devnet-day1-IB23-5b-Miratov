import json, os, subprocess
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "day5"
SCHEMA = ROOT / "schemas" / "day5_summary.schema.json"

def jload(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_day5_summary_and_evidence():
    env = os.environ.copy()
    assert env.get("STUDENT_TOKEN")
    assert env.get("STUDENT_NAME")
    assert env.get("STUDENT_GROUP")

    r = subprocess.run(["python3", "src/day5_summary_builder.py"], cwd=str(ROOT), env=env, capture_output=True, text=True)
    assert r.returncode in (0, 2), r.stderr

    summary = jload(ART / "summary.json")
    schema = jload(SCHEMA)
    jsonschema.validate(instance=summary, schema=schema)

    assert summary["yang"]["ok"] is True
    assert summary["webex"]["ok"] is True
    assert summary["pt"]["empty_ticket_seen"] is True
