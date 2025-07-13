import sys
import os

# Add project root
sys.path.insert(0, "/opt/SELFIX")

from ai_modules.selfix_mission_context import MissionContext
from ai_modules.ai_frontend_utils import generate_frontend_with_ollama, save_generated_html
import json
import logging
from datetime import datetime

LOG_PATH = "/opt/SELFIX/logs/seeder.log"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SEED_FILE = "/opt/SELFIX/data/seed_prompts.json"

def load_seed_prompts():
    if not os.path.exists(SEED_FILE):
        default_prompts = [
            {"label": "Landing Page", "prompt": "Create a landing page with TailwindCSS"},
            {"label": "Portfolio", "prompt": "Portfolio page with cards and a contact form"}
        ]
        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
        with open(SEED_FILE, "w") as f:
            json.dump(default_prompts, f, indent=4)
        return default_prompts
    else:
        with open(SEED_FILE, "r") as f:
            return json.load(f)

def run_seeder():
    ctx = MissionContext()
    seeds = load_seed_prompts()

    for seed in seeds:
        label = seed["label"]
        prompt = seed["prompt"]
        logging.info(f"🌱 Seeding: {label}")

        try:
            output = generate_frontend_with_ollama(prompt)
            filename = f"{label.lower().replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html"
            path = save_generated_html(output, filename)
            ctx.update("last_prompt", prompt)
            ctx.mark_generated(prompt)
            logging.info(f"✅ Saved: {path}")
        except Exception as e:
            logging.error(f"❌ Error seeding {label}: {e}")

if __name__ == "__main__":
    run_seeder()
