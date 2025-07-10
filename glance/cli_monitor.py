import time
import os
import requests
from datetime import datetime, timedelta
from rich.live import Live
from rich.table import Table
from rich.console import Console
from collections import defaultdict

LOG_PATH = "/opt/SELFIX/logs/mock_hq_requests.log"
STATUS_URL = "http://127.0.0.1:5000/status"
HELP_TIMEOUT_SECONDS = 60

console = Console()

# Runtime state
active_agents = {}
feature_usage = defaultdict(int)
last_log_line = ""

def fetch_seeder_status():
    try:
        response = requests.get(STATUS_URL, timeout=2)
        data = response.json()
        return "ON" if data.get("seeder_running") else "OFF"
    except Exception:
        return "UNKNOWN"

def parse_log():
    global last_log_line
    if not os.path.exists(LOG_PATH):
        return

    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()
            if not lines:
                return
            last = lines[-1].strip()
            if last == last_log_line:
                return
            last_log_line = last

            timestamp = last.split("]")[0].strip("[")
            log_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            data_part = last.split(":", 1)[-1].strip()
            data = eval(data_part)  # Expecting a dict

            agent_id = data.get("agent_id", "unknown")
            feature = data.get("feature", "unknown")
            status = data.get("status", "ok")

            # Update agent info
            active_agents[agent_id] = {
                "last_seen": log_time,
                "status": status
            }

            # Track feature usage
            feature_usage[feature] += 1

    except Exception as e:
        pass  # Silently fail on parse issues

def make_table():
    parse_log()

    table = Table(title="🛰️  SELFIX HQ - CLI Monitor", expand=True)

    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    # Seeder agent
    table.add_row("Seeder Agent", fetch_seeder_status())

    # Last log entry
    table.add_row("Last Log", last_log_line or "No logs yet")

    # Agent statuses with lights
    if active_agents:
        agent_lines = []
        now = datetime.utcnow()
        for agent_id, info in sorted(active_agents.items()):
            last_seen = info["last_seen"]
            status = info["status"]
            time_diff = (now - last_seen).total_seconds()

            if status == "help" or time_diff > HELP_TIMEOUT_SECONDS:
                light = "🔴"
                reason = "needs help" if status == "help" else "no contact"
            else:
                light = "🟢"
                reason = f"{int(time_diff)}s ago"

            agent_lines.append(f"{light} {agent_id} ({reason})")

        table.add_row("Agent Statuses", "\n".join(agent_lines))
    else:
        table.add_row("Agent Statuses", "No agents online")

    # Feature usage
    usage_summary = ", ".join(
        f"{f[-2:]}:{count}" for f, count in sorted(feature_usage.items()) if f.startswith("feature")
    ) or "No usage"
    table.add_row("Feature Usage", usage_summary)

    # Time
    table.add_row("Updated", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

    return table

if __name__ == "__main__":
    with Live(make_table(), refresh_per_second=1, console=console) as live:
        while True:
            time.sleep(2)
            live.update(make_table())
