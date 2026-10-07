import json
import time
from pathlib import Path

# ====================================================
# INPUT (Mordor Dataset)
# ====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "mordor_sample.json"

# VMware Shared Folder
OUTPUT_FILE = Path(r"C:\WazuhShared\mordor.log")

print("=" * 60)
print("Checking Mordor dataset")
print(INPUT_FILE)
print("=" * 60)

if not INPUT_FILE.exists():
    raise FileNotFoundError(INPUT_FILE)

# Clear previous output
OUTPUT_FILE.write_text("", encoding="utf-8")

# ====================================================
# LOAD NDJSON (JSON Lines)
# ====================================================

logs = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:

        line = line.strip()

        if not line:
            continue

        try:
            logs.append(json.loads(line))
        except json.JSONDecodeError:
            print("Skipped invalid line")

print(f"\nLoaded {len(logs)} Mordor logs")
print("Replaying to Wazuh...\n")

# ====================================================
# SEND TO WAZUH
# ====================================================

for i, log in enumerate(logs, start=1):

    with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
        out.write(json.dumps(log))
        out.write("\n")

    print(f"[{i}/{len(logs)}] Sent EventID={log.get('EventID')}")

    time.sleep(1)

print("\nReplay Complete!")