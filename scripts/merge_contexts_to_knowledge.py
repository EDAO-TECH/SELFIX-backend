import os
import json
from datetime import datetime

# Define source and target paths
DATA_DIR = "/opt/SELFIX/data"
MODULES_DIR = "/opt/SELFIX/ai_modules"
TARGET_PATH = os.path.join(DATA_DIR, "knowledge_context.json")

# Paths to be merged
context_files = [
    os.path.join(MODULES_DIR, "selfix_mission_context.json"),
    os.path.join(MODULES_DIR, "daily_learning_input.json"),
    os.path.join(DATA_DIR, "mission_context.json"),
]

# Initialize final context
merged_context = {
    "mission": "SELFIX Intelligence Core",
    "status": "active",
    "log": [],
    "learning_objectives": [],
    "last_digest": datetime.utcnow().isoformat()
}

def load_json(path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            with open(path) as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON in {path}")
    return {}

for path in context_files:
    data = load_json(path)

    # Pull top-level goal or mission
    if "goal" in data:
        merged_context["mission"] = data["goal"]
    elif "mission" in data:
        merged_context["mission"] = data["mission"]

    # Merge learning inputs
    if isinstance(data, list):
        merged_context["learning_objectives"].extend(data)
    elif "learning_objectives" in data:
        merged_context["learning_objectives"].extend(data["learning_objectives"])

    # Merge logs if present
    if "log" in data and isinstance(data["log"], list):
        merged_context["log"].extend(data["log"])

    # Include token details if any
    if "token" in data:
        merged_context["token"] = data["token"]

# Remove duplicates from learning objectives
merged_context["learning_objectives"] = list(set(merged_context["learning_objectives"]))

# Save merged context
os.makedirs(DATA_DIR, exist_ok=True)
with open(TARGET_PATH, "w") as f:
    json.dump(merged_context, f, indent=4)

print(f"✅ Merged context saved to {TARGET_PATH}")
