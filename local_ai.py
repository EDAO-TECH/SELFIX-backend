import sys
import os
sys.path.insert(0, "/opt/SELFIX")

from ai_modules.selfix_mission_context import MissionContext
from ai_modules.ai_frontend_utils import generate_frontend_with_ollama, save_generated_html

if __name__ == "__main__":
    ctx = MissionContext()
    prompt = ctx.get("last_prompt", "Create a basic responsive landing page using HTML and TailwindCSS.")

    print(f"🧠 Prompt: {prompt}")

    try:
        html = generate_frontend_with_ollama(prompt)
        path = save_generated_html(html)
        print(f"✅ Saved to {path}")
        ctx.mark_generated(prompt)
    except Exception as e:
        print(f"❌ Error: {e}")
