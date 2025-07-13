import schedule
import time
from local_ai import generate_frontend_with_ollama

def run_ai_job():
    prompt = "Create a responsive HTML landing page with TailwindCSS, navbar, hero section, and footer."
    result = generate_frontend_with_ollama(prompt)
    with open("frontend/generated/auto_page.html", "w") as f:
        f.write(result)
    print("✅ AI-generated frontend saved.")

# Run every hour
schedule.every(1).hours.do(run_ai_job)

while True:
    schedule.run_pending()
    time.sleep(10)
