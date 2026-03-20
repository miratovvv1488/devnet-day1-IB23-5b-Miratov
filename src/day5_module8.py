#!/usr/bin/env python3
import hashlib, json, os, requests
from pathlib import Path

TOKEN = os.getenv("WEBEX_TOKEN", "")
STUDENT_TOKEN = os.getenv("STUDENT_TOKEN", "")
TH8 = hashlib.sha256(STUDENT_TOKEN.encode()).hexdigest()[:8]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
BASE = "https://webexapis.com/v1"
ART = Path("artifacts/day5/webex")
ART.mkdir(parents=True, exist_ok=True)

def save(name, data):
    (ART / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {name}")

# 1. Me
me = requests.get(f"{BASE}/people/me", headers=HEADERS).json()
save("me.json", me)

# 2. Rooms list
rooms = requests.get(f"{BASE}/rooms", headers=HEADERS).json()
save("rooms_list.json", rooms)

# 3. Create room
room = requests.post(f"{BASE}/rooms", headers=HEADERS, json={"title": f"Lab Room {TH8}"}).json()
save("room_create.json", room)
room_id = room.get("id", "")

# 4. Post message
msg = requests.post(f"{BASE}/messages", headers=HEADERS, json={
    "roomId": room_id,
    "text": f"Hello from Miratov Mursalim TOKEN_HASH8={TH8}"
}).json()
save("message_post.json", msg)

# 5. Messages list
msgs = requests.get(f"{BASE}/messages?roomId={room_id}", headers=HEADERS).json()
save("messages_list.json", msgs)

print("Done! token_hash8 =", TH8)
