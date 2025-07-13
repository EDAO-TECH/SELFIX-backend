import os
import sys
import json
import subprocess

BASE_DIR = "/opt/SELFIX"
AGENTS_FILE = os.path.join(BASE_DIR, "ai_tower", "agents_registry.json")
GROUPS_FILE = os.path.join(BASE_DIR, "ai_tower", "groups.json")

def load_agents():
    with open(AGENTS_FILE, "r") as f:
        return json.load(f)

def load_groups():
    with open(GROUPS_FILE, "r") as f:
        return json.load(f)

def display_agents(agents):
    print("\n🤖 Registered AI Agents:\n")
    for agent_id, meta in agents.items():
        print(f"{agent_id}: {meta['name']} [{meta['type']}]")
        print(f"  ├─ Script     : {meta['script']}")
        print(f"  ├─ Description: {meta['description']}")
        print(f"  └─ Status     : {meta['status']}\n")

def run_agent(agent_id, agents, phase=None):
    if agent_id not in agents:
        print(f"❌ Agent {agent_id} not found.")
        return

    script_path = os.path.join(BASE_DIR, agents[agent_id]["script"])
    if not os.path.isfile(script_path):
        print(f"❌ Script not found: {script_path}")
        return

    print(f"🚀 Running {agent_id} - {agents[agent_id]['name']} ({phase if phase else 'default'})")
    if phase:
        subprocess.run(["python3", script_path, phase])
    else:
        subprocess.run(["python3", script_path])

def run_group(group_name, agents, groups, phase=None):
    if group_name not in groups:
        print(f"❌ Group {group_name} not defined.")
        return

    for agent_id in groups[group_name]:
        run_agent(agent_id, agents, phase)

def main():
    agents = load_agents()
    groups = load_groups()

    display_agents(agents)

    while True:
        choice = input("▶️ Enter Agent ID or Group (or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            break
        elif choice in groups:
            phase = input("🧠 Enter study phase (theory/practical): ").strip()
            run_group(choice, agents, groups, phase)
        else:
            run_agent(choice, agents)

if __name__ == "__main__":
    main()
