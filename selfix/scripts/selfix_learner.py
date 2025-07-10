#!/usr/bin/env python3

import json
import os
from datetime import datetime

DAILY_LOG = "/opt/SELFIX/ai_modules/daily_learning_input.json"
MISSION_CONTEXT = "/opt/SELFIX/ai_modules/selfix_mission_context.json"
LEARNING_LOG = "/opt/SELFIX/logs/learning_events.log"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Warning: Failed to load {path}")
            return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def log_learning_event(msg):
    with open(LEARNING_LOG, "a") as log:
        log.write(f"[{datetime.now().isoformat()}] {msg}\n")

def main():
    print("🧠 Starting Selfix Learner...")
    
    daily_data = load_json(DAILY_LOG, [])
    if not daily_data:
        print("⚠️ No data to learn from.")
        return

    context = load_json(MISSION_CONTEXT, {
        "threat_signatures": {},
        "learning_history": []
    })

    learned = 0
    for entry in daily_data:
        content = entry.get("content", "")
        src = entry.get("source", "unknown")

        # Simple learning rule: increase tag weight if keyword is known
        for threat_tag in ["malware", "backdoor", "scan-failure", "entropy-warning", "unauthorized-access"]:
            if threat_tag in content.lower():
                current_weight = context["threat_signatures"].get(threat_tag, 0)
                context["threat_signatures"][threat_tag] = current_weight + 1
                learned += 1
                log_learning_event(f"📈 Reinforced tag '{threat_tag}' from {src}")

    context["learning_history"].append({
        "timestamp": datetime.now().isoformat(),
        "learned_from": DAILY_LOG,
        "entries_processed": len(daily_data),
        "threat_tags_updated": learned
    })

    save_json(MISSION_CONTEXT, context)
    print(f"✅ Learning complete. {learned} threat weights updated.")
    log_learning_event("✅ Learning session completed successfully.")

if __name__ == "__main__":
    main()
