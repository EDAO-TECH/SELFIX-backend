# /opt/SELFIX/api/main_api.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import os
import json
from datetime import datetime

app = FastAPI(title="SELFIX Defense API", version="1.0")

# ────────────────────────────────────────────────
# 🌐 CORS SETUP – allow frontend to connect
# ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace with ["https://your-horizon-site.com"] in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────────────────────────────
# 📦 Utility: Load JSON from file
# ────────────────────────────────────────────────
def load_json(filepath, fallback=None):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return fallback if fallback is not None else {}

# ────────────────────────────────────────────────
# 📡 Endpoint: System Status
# ────────────────────────────────────────────────
@app.get("/api/status")
def get_status():
    status_data = load_json("/opt/SELFIX/data/system_status.json", {
        "status": "UNKNOWN",
        "healing_active": False,
    })
    return {
        "system": "SELFIX",
        "status": status_data.get("status", "UNKNOWN"),
        "healing_active": status_data.get("healing_active", False),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# ────────────────────────────────────────────────
# 🧠 Endpoint: AI Journal Snapshot (optional)
# ────────────────────────────────────────────────
@app.get("/api/ai-journal")
def get_journal():
    journal = load_json("/opt/SELFIX/data/ai_journal.json", {})
    return {"journal": journal}

# ────────────────────────────────────────────────
# 🔍 Endpoint: Last 20 Entropy Events
# ────────────────────────────────────────────────
@app.get("/api/entropy")
def get_entropy_events():
    path = "/opt/SELFIX/logs/healing_daemon.log"
    entries = []
    try:
        with open(path, "r") as f:
            lines = f.readlines()[-20:]
            for line in lines:
                try:
                    entries.append(json.loads(line.strip()))
                except:
                    continue
    except FileNotFoundError:
        pass
    return {"events": entries}

# ────────────────────────────────────────────────
# 🔐 Optional health check
# ────────────────────────────────────────────────
@app.get("/api/ping")
def ping():
    return {"pong": True, "timestamp": datetime.utcnow().isoformat() + "Z"}

# ────────────────────────────────────────────────
# ⚠️ Error handler (optional)
# ────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={
        "error": str(exc),
        "path": request.url.path
    })
