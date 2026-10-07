import json
import os

from alert_parser import parse_alert
from config import ALERT_FILE, PROCESSED_FILE


# ============================================================
# Load processed alert IDs
# ============================================================

def load_processed():
    if not os.path.exists(PROCESSED_FILE):
        return set()

    with open(PROCESSED_FILE, "r") as f:
        return set(line.strip() for line in f)


# ============================================================
# Save processed alert ID
# ============================================================

def save_processed(alert_id):
    with open(PROCESSED_FILE, "a") as f:
        f.write(alert_id + "\n")


# ============================================================
# Main
# ============================================================

processed = load_processed()

print("\nReading Wazuh Alerts...\n")

if not os.path.exists(ALERT_FILE):
    print("ERROR: alerts.json not found!")
    exit()

with open(ALERT_FILE, "r", encoding="utf-8") as f:

    for line in f:

        line = line.strip()

        # Skip blank lines
        if not line:
            continue

        # Skip invalid JSON
        try:
            alert = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Get alert ID
        alert_id = alert.get("id")

        if not alert_id:
            continue

        # Skip processed alerts
        if alert_id in processed:
            continue

        # ==========================================
        # Parse alert
        # ==========================================

        parsed = parse_alert(alert)
                # ==========================================
        # ONLY PROCESS HEALTHCARE ALERTS
        # ==========================================

        rule = alert.get("rule", {})
        rule_id = str(rule.get("id", ""))

        HEALTHCARE_RULES = {
            "100100",   # FTP
            "100101",   # SSH
            "100102",   # Port Scan
            "100103",   # DDoS
        }

        if rule_id not in HEALTHCARE_RULES:
            continue
                # ==========================================
        # Save latest alert for the RAG pipeline
        # ==========================================

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        current_alert_path = os.path.join(
            BASE_DIR,
            "data",
            "current_alert.json"
        )

        with open(current_alert_path, "w", encoding="utf-8") as outfile:
            json.dump(parsed, outfile, indent=4)
                    # ==========================================
        # Append alert for Dashboard History
        # ==========================================

        alerts_path = os.path.join(
            BASE_DIR,
            "data",
            "alerts.json"
        )

        with open(
            alerts_path,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(json.dumps(parsed))
            f.write("\n")
        print("=" * 70)
        print("NEW WAZUH ALERT")
        print("=" * 70)

        for key, value in parsed.items():
            print(f"{key:<15}: {value}")

        print()

        save_processed(alert_id)
            
        
        

        # ==========================================
        # Save latest alert for the RAG pipeline
        # ==========================================

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        current_alert_path = os.path.join(
            BASE_DIR,
            "data",
            "current_alert.json"
        )

        with open(current_alert_path, "w", encoding="utf-8") as outfile:
            json.dump(parsed, outfile, indent=4)
                    # ==========================================
        # Append alert for Dashboard History
        # ==========================================

        alerts_path = os.path.join(
            BASE_DIR,
            "data",
            "alerts.json"
        )

        with open(
            alerts_path,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(json.dumps(parsed))
            f.write("\n")
            
            

        print("=" * 70)
        print("NEW WAZUH ALERT")
        print("=" * 70)

        for key, value in parsed.items():
            print(f"{key:<15}: {value}")

        print()

        save_processed(alert_id)

print("\nFinished checking alerts.")