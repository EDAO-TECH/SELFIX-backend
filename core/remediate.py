#!/usr/bin/env python3

import os
import json
from pathlib import Path
from datetime import datetime
from core.quarantine_module import quarantine_file

VAULT_HASHES = Path("/opt/SELFIX/data/vault_hashes.json")
QUARANTINE = Path("/opt/SELFIX/quarantine")


def suggest_action(file, match=None, entropy=None, karma=None):
    if match and "Trojan" in match:
        return "quarantine"
    if entropy and entropy > 0.85:
        return "quarantine"
    if karma and karma < 0.3:
        return "quarantine"
    return "monitor"


def remediate(file_report):
    file = file_report.get("file")
    match = file_report.get("signature")
    entropy = file_report.get("entropy")
    karma = file_report.get("karma")

    action = suggest_action(file, match, entropy, karma)
    log = {
        "file": file,
        "reason": {
            "signature": match,
            "entropy": entropy,
            "karma": karma
        },
        "suggested_action": action,
        "timestamp": datetime.utcnow().isoformat()
    }

    if action == "quarantine":
        result = quarantine_file(file)
        log.update({"executed_action": "quarantine", "result": result})
    else:
        log.update({"executed_action": "none"})

    return log


if __name__ == "__main__":
    example = {
        "file": "/home/user/suspicious.sh",
        "signature": "Trojan.Generic",
        "entropy": 0.92,
        "karma": 0.2
    }
    report = remediate(example)
    print(json.dumps(report, indent=2))
