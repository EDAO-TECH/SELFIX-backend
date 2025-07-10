import json
import sys
import os
from datetime import datetime

# Add /opt/SELFIX/ to the import path so entropy_resolver works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entropy_resolver import run_entropy_check
from scripts.vpn_check import vpn_check
from scripts.agent_002_check import agent_check
from scripts.simple_health_check import status as hw_status
from entropy_resolver import run_entropy_check

status = {
    "timestamp": str(datetime.utcnow()),
    "status": "pending",
    "system_mode": "unknown",
    "healing_active": False,
    "components": {},
    "entropy_score": None,
    "agent_version": "002-final"
}

# Inherit from simple_health_check
status["components"]["hardware_check"] = "pass" if hw_status["hardware_ok"] else "fail"

# Run VPN
status["components"]["vpn_check"] = vpn_check()

# Run entropy
entropy_ok, entropy_score = run_entropy_check()
status["components"]["entropy_check"] = "pass" if entropy_ok else "fail"
status["entropy_score"] = entropy_score

# Run agent check
status["components"]["agent_002_check"] = agent_check()

# Final decision
if all(v == "pass" for v in status["components"].values()):
    status["status"] = "greenlight"
    status["system_mode"] = "autonomous"
    status["healing_active"] = True
else:
    status["status"] = "blocked"
    status["system_mode"] = "passive_monitor"

# Save result
with open("/opt/SELFIX/data/selfix_precheck_status.json", "w") as f:
    json.dump(status, f, indent=4)

print("🟢 Precheck Complete. System Mode:", status["system_mode"])

