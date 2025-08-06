import json
import subprocess
import sys
from datetime import datetime
import os

REGISTRY_PATH = "/opt/SELFIX/ai_tower/agents_registry.json"
STUDY_LOG_DIR = "/opt/SELFIX/logs"
CURRICULUM_DIR = "/opt/SELFIX/ai_tower"

def load_agents():
    with open(REGISTRY_PATH) as f:
        return json.load(f)

def run_agent(agent_id, agent):
    script = f"/opt/SELFIX/{agent['script']}"
    phase = sys.argv[1] if len(sys.argv) > 1 else "practical"
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_folder = f"{STUDY_LOG_DIR}/{phase}"
    os.makedirs(log_folder, exist_ok=True)
    log_path = f"{log_folder}/{agent_id}_{timestamp}.log"

    print(f"🧠 Running {agent['name']} ({agent_id}) in {phase} mode...")
    try:
        result = subprocess.run(
            ["python3", script, phase],
            capture_output=True, text=True, timeout=300
        )
        with open(log_path, "w") as f:
            f.write(result.stdout + "\n" + result.stderr)
        print(f"✅ Output saved to {log_path}")
    except Exception as e:
        print(f"❌ Error running {agent['name']}: {str(e)}")

def main():
    agents = load_agents()
    for agent_id, agent in agents.items():
        if agent.get("status") == "active":
            run_agent(agent_id, agent)

if __name__ == "__main__":
    main()
