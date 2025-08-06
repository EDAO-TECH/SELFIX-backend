import os
import json
from datetime import datetime

BASE_DIR = "/opt/SELFIX"
CONTEXT_FILE = os.path.join(BASE_DIR, "ai_modules", "selfix_mission_context.json")
DIGEST_FILE = os.path.join(BASE_DIR, "ai_tower", "theory_education", "daily_digest.md")

def read_context():
    with open(CONTEXT_FILE, "r") as f:
        return json.load(f)

def summarize_section(title, content):
    if isinstance(content, list):
        return f"### {title}\n" + "\n".join(f"- {item}" for item in content) + "\n"
    elif isinstance(content, dict):
        summary = f"### {title}\n"
        for k, v in content.items():
            summary += f"- **{k}**: {v}\n"
        return summary + "\n"
    else:
        return f"### {title}\n{content}\n"

def build_digest(data):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    sections = [f"\n\n## 📘 SELFIX Study Digest — {today}\n"]

    # Mandatory core
    sections.append(summarize_section("Mission Goal", data.get("goal", "[No goal]")))
    sections.append(summarize_section("Current Status", data.get("status", "[No status]")))
    sections.append(summarize_section("Log", data.get("log", [])))
    sections.append(summarize_section("Next Steps", data.get("next_steps", [])))

    # Optional deeper learnings
    if "ip_chain" in data:
        sections.append(summarize_section("IP Chain & NFT Plan", data["ip_chain"]))
    if "defi_finance" in data:
        sections.append(summarize_section("DeFi Strategy", data["defi_finance"]))

    sections.append("🧠 _Digest compiled from mission context for agent education._")
    return "\n".join(sections)

def append_digest(text):
    os.makedirs(os.path.dirname(DIGEST_FILE), exist_ok=True)
    with open(DIGEST_FILE, "a") as f:
        f.write(text + "\n")

if __name__ == "__main__":
    try:
        data = read_context()
        digest = build_digest(data)
        append_digest(digest)
        print(f"✅ Digest written to: {DIGEST_FILE}")
    except Exception as e:
        print(f"❌ Failed: {e}")
