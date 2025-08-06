import os
import datetime

LOGS_DIR = "/opt/SELFIX/logs"
REFLECTION_LOG = os.path.join(LOGS_DIR, "reflections.log")

def list_recent_logs(phase_dir, max_files=5):
    path = os.path.join(LOGS_DIR, phase_dir)
    if not os.path.exists(path):
        return []
    files = sorted(os.listdir(path), reverse=True)[:max_files]
    return [os.path.join(path, f) for f in files]

def extract_summary(log_path):
    with open(log_path, "r") as f:
        lines = f.readlines()
    content = "".join(lines[-10:])
    return f"📄 {os.path.basename(log_path)}:\n{content}\n"

def main():
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    reflections = [f"\n🪞 Daily Reflection - {now}\n"]

    for phase in ["theory", "practical"]:
        reflections.append(f"\n📚 Phase: {phase.upper()}")
        logs = list_recent_logs(phase)
        for log in logs:
            reflections.append(extract_summary(log))

    with open(REFLECTION_LOG, "a") as f:
        f.write("\n".join(reflections) + "\n" + ("="*40) + "\n")

if __name__ == "__main__":
    main()
