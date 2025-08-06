import os, json, subprocess

AGENTS_PATH = "/opt/SELFIX/agents"
REGISTRY_PATH = "/opt/SELFIX/ai_tower/agents_registry.json"
CURRICULA_PATH = "/opt/SELFIX/ai_tower"

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)

def run_phase(agent_id, script, phase):
    log_dir = f"/opt/SELFIX/logs/{phase}"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{agent_id}.log")
    try:
        result = subprocess.run(
            ["python3", f"/opt/SELFIX/{script}", phase],
            capture_output=True,
            text=True,
            timeout=300
        )
        with open(log_file, "w") as f:
            f.write(result.stdout + "\n" + result.stderr)
        print(f"✅ {agent_id} {phase} complete.")
    except Exception as e:
        print(f"❌ Error for {agent_id}: {e}")

def main(phase="practical"):
    registry = load_registry()
    for agent_id, meta in registry.items():
        if meta["type"] == "seed-agent":
            continue  # Skip Seeder
        script = meta.get("script")
        if script:
            run_phase(agent_id, script, phase)

if __name__ == "__main__":
    import sys
    phase = sys.argv[1] if len(sys.argv) > 1 else "practical"
    main(phase)
