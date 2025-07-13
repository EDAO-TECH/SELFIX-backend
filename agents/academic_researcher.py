"""
Agent Role: Academic Researcher
SELFIX Core Identity:
  • Purpose: Source scholarly knowledge, generate informative content
  • New Roles:
      - Write website content based on research & business goals
      - Propose structure for frontend layout
  • Ethic Guardrails:
      - No fabricated citations
      - Respect copyright, provide fair-use summaries
  • SELFIX Principles:
      - Clarity, trust, and family-business integrity
"""

import sys
import json
from datetime import datetime

MISSION_CONTEXT_PATH = "/opt/SELFIX/data/mission_context.json"
WEBSITE_CONTENT_PATH = "/opt/SELFIX/frontend/generated/website_content.md"
WEBSITE_LAYOUT_PATH = "/opt/SELFIX/frontend/generated/website_layout.json"

def load_context():
    try:
        with open(MISSION_CONTEXT_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def generate_website_content(context):
    mission = context.get("mission", "Build trusted AI-powered business tools.")
    vision = context.get("vision", "To help users build sustainable, ethical businesses.")
    values = context.get("values", ["Trust", "Execution", "Empathy"])

    sections = {
        "About Us": f"SELFIX is a family-driven AI company. Our mission is: {mission}.",
        "Vision": vision,
        "Our Values": ", ".join(values),
        "Services": "- AI Agent Orchestration\n- Token/NFT Support\n- Frontend/App Development",
        "FAQ": "Q: What is SELFIX?\nA: SELFIX builds intelligent, ethical business agents powered by local AI models."
    }

    output = "# Website Content Draft\n\n"
    for title, body in sections.items():
        output += f"## {title}\n{body}\n\n"

    with open(WEBSITE_CONTENT_PATH, "w") as f:
        f.write(output)
    print(f"📝 Website content saved to {WEBSITE_CONTENT_PATH}")

def suggest_layout():
    layout = {
        "layout": [
            {"section": "hero", "type": "headline+cta", "content_ref": "About Us"},
            {"section": "features", "type": "grid", "items": ["Services", "Our Values"]},
            {"section": "vision", "type": "banner", "content_ref": "Vision"},
            {"section": "faq", "type": "accordion", "content_ref": "FAQ"}
        ],
        "generated": str(datetime.utcnow())
    }

    with open(WEBSITE_LAYOUT_PATH, "w") as f:
        json.dump(layout, f, indent=2)
    print(f"📐 Website layout proposal saved to {WEBSITE_LAYOUT_PATH}")

def run_theory():
    print("📚 Agent006: Performing academic-style research...")
    context = load_context()
    print(f"🔍 Researching based on mission: {context.get('mission', '[No Mission]')}")

def run_practical():
    print("✍️ Agent006: Writing website content and layout...")
    context = load_context()
    generate_website_content(context)
    suggest_layout()

if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "practical"
    if phase == "theory":
        run_theory()
    else:
        run_practical()
