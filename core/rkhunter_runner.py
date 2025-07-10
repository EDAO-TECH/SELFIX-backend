#!/usr/bin/env python3

import subprocess
import json
from datetime import datetime
from pathlib import Path

OUTPUT_LOG = Path("/opt/SELFIX/data/rootkit_scan.json")


def run_rkhunter():
    try:
        result = subprocess.run(
            ["rkhunter", "--check", "--sk", "--nocolors", "--rwo"],
            capture_output=True, text=True, check=True
        )
        findings = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        findings = [f"Error running rkhunter: {e.stderr.strip()}"]

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "findings": findings
    }

    OUTPUT_LOG.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_LOG.write_text(json.dumps(log, indent=2))
    return log


if __name__ == "__main__":
    report = run_rkhunter()
    print(json.dumps(report, indent=2))
