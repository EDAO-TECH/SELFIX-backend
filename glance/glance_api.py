from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict
import os
import ast

app = Flask(__name__)
LOG_PATH = "/opt/SELFIX/logs/mock_hq_requests.log"
SEEDER_STATE_PATH = "/opt/SELFIX/logs/seeder_state.txt"

# Utilities
def read_log_lines():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            return f.readlines()
    return []

def current_seeder_state():
    if os.path.exists(SEEDER_STATE_PATH):
        return open(SEEDER_STATE_PATH).read().strip()
    return "OFF"

def set_seeder_state(state):
    with open(SEEDER_STATE_PATH, "w") as f:
        f.write(state)

# ✅ 1. Health check
@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "✅ SELFIX HQ is live"})

# ✅ 2. Seeder agent status POST
@app.route("/api/seeder/status", methods=["POST"])
def seeder_status():
    try:
        data = request.get_json(force=True)
        source_ip = request.remote_addr
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        log_line = f"[{timestamp}] From {source_ip}: {data}\n"
        with open(LOG_PATH, "a") as f:
            f.write(log_line)
        return jsonify({"hq_status": "✅ Received"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ✅ 3. Seeder ON/OFF control
@app.route("/toggle-seeder", methods=["POST"])
def toggle_seeder():
    data = request.get_json()
    if not data or data.get("state") not in ["ON", "OFF"]:
        return jsonify({"error": "Invalid state"}), 400
    set_seeder_state(data["state"])
    return jsonify({"seeder_state": data["state"]})

# ✅ 4. Get Seeder ON/OFF state
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"seeder_running": current_seeder_state() == "ON"})

# ✅ 5. Agent health list
@app.route("/agent-health", methods=["GET"])
def agent_health():
    HELP_TIMEOUT = 60
    agents = {}
    now = datetime.utcnow()

    for line in reversed(read_log_lines()):
        if "]" not in line: continue
        timestamp = line.split("]")[0].strip("[")
        try:
            log_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            data_part = line.split(":", 1)[-1].strip()
            data = ast.literal_eval(data_part)
            agent_id = data.get("agent_id", "unknown")
            status = data.get("status", "ok")
            if agent_id not in agents:
                delta = (now - log_time).total_seconds()
                if status == "help":
                    light, reason = "red", "needs help"
                elif delta > HELP_TIMEOUT:
                    light, reason = "red", "no contact"
                else:
                    light, reason = "green", f"{int(delta)}s ago"
                agents[agent_id] = {"agent_id": agent_id, "light": light, "status": reason}
        except:
            continue

    return jsonify(list(agents.values()))

# ✅ 6. Single agent precheck for Horizon AI
@app.route("/precheck", methods=["GET"])
def precheck():
    agent_id = request.args.get("agent_id")
    if not agent_id:
        return jsonify({"error": "Missing agent_id"}), 400

    for line in reversed(read_log_lines()):
        if "]" not in line: continue
        timestamp = line.split("]")[0].strip("[")
        try:
            log_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            data_part = line.split(":", 1)[-1].strip()
            data = ast.literal_eval(data_part)
            if data.get("agent_id") == agent_id:
                delta = (datetime.utcnow() - log_time).total_seconds()
                if data.get("status") == "help":
                    return jsonify({"status": "red", "reason": "needs help"}), 503
                elif delta > 60:
                    return jsonify({"status": "red", "reason": "no contact"}), 503
                else:
                    return jsonify({"status": "green", "reason": f"{int(delta)}s ago"}), 200
        except:
            continue

    return jsonify({"status": "red", "reason": "not found"}), 503

# ✅ 7. Placeholder for /chat (to connect to Horizon AI backend later)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({
        "reply": f"(Simulated) AI response to: {message}"
    })

# ✅ 8. Feature usage summary
@app.route("/feature-usage", methods=["GET"])
def feature_usage():
    usage = defaultdict(int)
    for line in read_log_lines():
        try:
            data = ast.literal_eval(line.split(":", 1)[-1].strip())
            feature = data.get("feature", "unknown")
            usage[feature] += 1
        except:
            continue
    return jsonify(dict(usage))

# ✅ 9. Get latest log lines (preview only)
@app.route("/logs/latest", methods=["GET"])
def latest_logs():
    lines = read_log_lines()[-50:]
    return jsonify({"lines": lines})

# Run the app
if __name__ == "__main__":
    print("✅ Starting SELFIX API only mode on port 5000...")
    app.run(host="0.0.0.0", port=5000)
