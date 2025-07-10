#!/bin/bash

# ──── CONFIG ────
FASTAPI_PORT=8000
GPT_API_PORT=8825
SELFIX_DIR="/opt/SELFIX"
LOG_DIR="$SELFIX_DIR/logs"
DAEMON_SCRIPT="$SELFIX_DIR/scripts/daemon_loop.py"
LOCK_FILE="/tmp/selfix_start.lock"

mkdir -p "$LOG_DIR"

# ──── LOCKFILE GUARD ────
if [ -f "$LOCK_FILE" ]; then
    echo "🚫 Already running. Lockfile exists."
    exit 1
fi
touch "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# ──── RESOURCE INFO ────
cpu_usage=$(ps -A -o %cpu | awk '{s+=$1} END {print s}')
mem_usage=$(free | awk '/Mem:/ { printf("%.0f", ($3/$2)*100) }')
echo "🧐 CPU: ${cpu_usage}% | MEM: ${mem_usage}%"
echo "⚠️  Skipping CPU/MEM limits for debugging..."

# ──── CLEAN PREVIOUS PROCESSES ────
echo "🧼 Killing previous services..."
for proc in "uvicorn app.main:app" "gpt_api.py" "daemon_loop.py"; do
    pkill -f "$proc" 2>/dev/null && echo "✔ Killed: $proc"
done

# ──── START FASTAPI ────
echo "🚀 Starting FastAPI..."
cd "$SELFIX_DIR" || exit
nohup uvicorn api.main:app --host 0.0.0.0 --port $FASTAPI_PORT >> "$LOG_DIR/fastapi.log" 2>&1 &

# ──── START GPT API ────
echo "🤖 Starting GPT API..."
cd "$SELFIX_DIR/app" || exit
nohup python3 api/gpt_api.py >> "$LOG_DIR/gpt_api.log" 2>&1 &

# ──── STABILIZE ────
sleep 5

# ──── HEALTH CHECKS ────
fastapi_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$FASTAPI_PORT/health)
gpt_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$GPT_API_PORT/api/karma-score)

echo "📱 FastAPI Status: $fastapi_status"
echo "📱 GPT API Status: $gpt_status"

# ──── START DAEMON ────
echo "🦭 Launching Healing Daemon..."
cd "$SELFIX_DIR/scripts" || exit
nohup python3 daemon_loop.py >> "$LOG_DIR/daemon.log" 2>&1 &

echo "✅ All SELFIX services launched!"
echo "📁 Logs: $LOG_DIR"
