#!/usr/bin/env python3

from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = "/opt/SELFIX/logs/mock_hq_requests.log"

@app.route("/api/seeder/status", methods=["POST"])
def receive_status():
    data = request.json
    log_msg = f"[{datetime.now().isoformat()}] Received status from {data.get('hostname')}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_msg)
        f.write(str(data) + "\n\n")
    print(log_msg.strip())
    
    # Simulate a command response (you can customize this)
    return jsonify({
        "command": "none",
        "msg": "Received. No action required."
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
