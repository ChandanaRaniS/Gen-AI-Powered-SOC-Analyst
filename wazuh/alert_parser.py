"""
Convert a Wazuh alert into a format that our RAG understands.
"""

import json


def parse_alert(alert):

    parsed = {}

    # ==========================================================
    # Basic Wazuh Information
    # ==========================================================

    parsed["id"] = alert.get("id")

    parsed["timestamp"] = alert.get("timestamp")

    parsed["description"] = alert.get("rule", {}).get(
        "description",
        "Unknown Alert"
    )

    parsed["agent"] = alert.get("agent", {}).get(
        "name",
        ""
    )

    parsed["mitre"] = alert.get("mitre", {}).get(
        "id",
        []
    )

    parsed["technique"] = alert.get("mitre", {}).get(
        "technique",
        []
    )

    parsed["full_log"] = alert.get("full_log", "")

    # ==========================================================
    # Parse the Healthcare JSON stored inside full_log
    # ==========================================================

    try:

        full_log = json.loads(parsed["full_log"])

        parsed["attack_type"] = full_log.get(
            "attack_type",
            ""
        )

        parsed["severity"] = full_log.get(
            "severity",
            "Unknown"
        )

        parsed["system"] = full_log.get(
            "system",
            ""
        )

        parsed["destination_port"] = full_log.get(
            "destination_port",
            ""
        )

    except Exception:

        # Fallback if full_log is not valid JSON

        parsed["attack_type"] = ""

        parsed["severity"] = alert.get("rule", {}).get(
            "level",
            ""
        )

        parsed["system"] = ""

        parsed["destination_port"] = ""

    return parsed