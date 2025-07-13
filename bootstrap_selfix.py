#!/usr/bin/env python3

import os
import json
import sys

BASE_DIR = "/opt/SELFIX"
DIRS = [
    "data",
    "logs",
    "frontend/generated",
    "agents",
    "ai_modules"
]

FILES = {
    "data/mission_context.json": {
        "mission": "frontend_generation",
        "status": "ready",
        "last_prompt": "Create a basic responsive landing page using HTML and TailwindCSS.",
        "last_generated": None,
        "meta": {
            "version": "1.0.0",
            "source": "selfix_ai"
        }
    },
    "data/seed_prompts.json": [
        {
            "label": "Landing Page",
            "prompt": "Create a clean responsive landing page with TailwindCSS including hero, features, and footer."
        },
        {
            "label": "Portfolio",
            "prompt": "Generate a personal portfolio site in HTML and Tailwind with project cards and a contact form."
        },
        {
            "label": "Pricing Page",
            "prompt": "Build a responsive pricing page layout with three pricing tiers and feature comparison."
        }
    ],
    "logs/seeder.log": "Seeder log initialized.\n",
    "logs/mission_context.log": "Mission context log initialized.\n"
}

def ensure_dirs():
    for d in DIRS:
        full_path = os.path.join(BASE_DIR, d)
        os.makedirs(full_path, exist_ok=True)
        print(f"✅ Created directory: {full_path}")

def ensure_files():
    for relative_path, content in FILES.items():
        full_path = os.path.join(BASE_DIR, relative_path)
        if not os.path.exists(full_path) or os.path.getsize(full_path) == 0:
            with open(full_path, "w") as f:
                if isinstance(content, (dict, list)):
                    json.dump(content, f, indent=4)
                else:
                    f.write(content)
            print(f"✅ Created: {full_path}")
        else:
            print(f"✔️ Exists: {full_path}")

def patch_python_paths():
    launcher_path = os.path.join(BASE_DIR, "ai_modules", "ai_frontend_utils.py")
    if not os.path.exists(launcher_path):
        print(f"⚠️ Missing core module: {launcher_path}")
    else:
        print(f"✔️ Python modules present")

def run_repair():
    print("🔧 Repairing SELFIX environment...")
    ensure_dirs()
    ensure_files()
    patch_python_paths()
    print("✅ All done. You can now run the Seeder or AI runner.")

if __name__ == "__main__":
    if "--repair" in sys.argv:
        run_repair()
    else:
        print("Usage: python3 bootstrap_selfix.py --repair")
