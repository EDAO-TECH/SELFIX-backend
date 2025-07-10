from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime

app = Flask(__name__)

# Log file for receiving status from agents
LOG_PATH = "/opt/SELFIX/logs/mock_hq_requests.log"

# Track Seeder status in memory
is_seeder_running = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/seeder/status", methods=["POST"])
def seeder_status():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "details": str(e)}), 400

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    source_ip = request.remote_addr

    log_entry = f"[{timestamp}] From {source_ip}: {data}\n"

    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    # Append log
    with open(LOG_PATH, "a") as log_file:
        log_file.write(log_entry)

    return jsonify({"hq_status": "✅ Received"}), 200

@app.route('/toggle-seeder', methods=['POST'])
def toggle_seeder():
    global is_seeder_running
    action = request.json.get('action')
    if action == 'on':
        is_seeder_running = True
        return jsonify({'status': 'Seeder started'})
    elif action == 'off':
        is_seeder_running = False
        return jsonify({'status': 'Seeder stopped'})
    return jsonify({'error': 'Invalid action'}), 400

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    return jsonify({'reply': f"You said: {user_message}"})

@app.route('/status')
def status():
    return jsonify({'seeder_running': is_seeder_running})

if __name__ == "__main__":
    print("✅ Starting SELFIX HQ Glance (port 5000)...")
    app.run(host="0.0.0.0", port=5000)
