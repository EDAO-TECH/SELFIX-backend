#!/bin/bash

# ───────────────────────────────────────────────
# 🧠 SELFIX Smart Startup Script
# Safely boots FastAPI, GPT API, and Healing Daemon
# Prevents duplicates, logs health, and stabilizes state
# ───────────────────────────────────────────────

# ── CONFIG ──────────────────────────────────────
FASTAPI_PORT=8000
GPT_API_PORT=8825
LOG_DIR="/opt/SELFIX/logs"
DAEMON_LOG="$LOG_DIR/daemon.log"
FASTAPI_LOG="$LOG_DIR/fastapi.log"
GPT_API_LOG="$LOG_DIR/gpt_api.log"
DAEMON_SCRIPT="/opt/SELFIX/scripts/daemon_loop.py"
LOCK_FILE="/tmp/selfix_start.lock"
CPU_THRESHOLD=80
MEM_THRESHOLD=80

mkdir -p "$LOG_DIR"

# ── PREVENT DUPLICATE RUN ──────────────────────
if [ -f "$LOCK_FILE" ]; then
    echo "🚫 Startup already running (lockfile exists). Exiting."
    exit 1
fi
touch "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# ── RESOURCE CHECK ─────────────────────────────

cpu_usage=$(top -bn1 | awk '/%Cpu/ {print 100 - $8}')
mem_usage=$(free | awk '/Mem:/ {printf("%.0f", ($3/$2)*100)}')

echo "🧠 CPU: $cpu_usage% | MEM: $mem_usage%"

if (( $(echo "$cpu_usage > $CPU_THRESHOLD" | bc -l) )); then
    echo "❌ CPU too high ($cpu_usage%). Aborting startup."
    exit 1
fi

if (( mem_usage > MEM_THRESHOLD )); then
    echo "❌ Memory too high ($mem_usage%). Aborting startup."
    exit 1
fi

# ── CLEANUP OLD PROCESSES ──────────────────────
echo "🧼 Cleaning up old services..."
for proc in "uvicorn app.main:app" "gpt_api.py" "daemon_loop.py"; do
    pkill -9 -f "$proc" && echo "✔ Killed: $proc"
done

# ── START FASTAPI ──────────────────────────────
echo "🚀 Starting FastAPI (port $FASTAPI_PORT)..."
cd /opt/SELFIX
nohup /opt/SELFIX/venv/bin/uvicorn app.main:app \
    --host 0.0.0.0 --port $FASTAPI_PORT --workers 1 \
    >> "$FASTAPI_LOG" 2>&1 &

# ── START GPT API ──────────────────────────────
echo "🤖 Starting GPT Flask API (port $GPT_API_PORT)..."
cd /opt/SELFIX/app
nohup /opt/SELFIX/venv/bin/python3 api/gpt_api.py \
    >> "$GPT_API_LOG" 2>&1 &

# ── STABILIZE ──────────────────────────────────
echo "⏳ Waiting for services to stabilize..."
sleep 10

# ── HEALTH CHECK ───────────────────────────────
fastapi_status=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$FASTAPI_PORT/health)
gpt_status=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$GPT_API_PORT/api/karma-score -H "Stripe-Token: test" || echo "000")

echo "📡 FastAPI: HTTP $fastapi_status"
echo "📡 GPT API: HTTP $gpt_status"

# ── START HEALING DAEMON IF NEEDED ─────────────
if pgrep -f "daemon_loop.py" > /dev/null; then
    echo "🧬 Healing Daemon already running."
else
    echo "🧬 Starting Healing Daemon..."
    nohup /opt/SELFIX/venv/bin/python3 "$DAEMON_SCRIPT" \
        >> "$DAEMON_LOG" 2>&1 &
fi

# ── DONE ───────────────────────────────────────
echo "✅ All SELFIX services launched successfully."
echo "📁 Logs: $LOG_DIR"

# ── LAUNCH REALTIME CLI MONITOR ────────────────
GLANCE_CLI="/opt/SELFIX/glance/glance_cli.py"

if [ -f "$GLANCE_CLI" ]; then
    echo "📊 Starting Realtime CLI Monitor..."
    if [ -t 1 ]; then
        # Running in terminal
        /opt/SELFIX/venv/bin/python3 "$GLANCE_CLI"
    else
        # Headless or service call
        nohup /opt/SELFIX/venv/bin/python3 "$GLANCE_CLI" \
            >> "$LOG_DIR/glance_cli.out" 2>&1 &
    fi
else
    echo "⚠️ Glance CLI not found at $GLANCE_CLI"
fi
