#!/bin/bash

# === SELFIX RUNTIME CLEANUP SCRIPT ===
# Logs all cleanup operations and maintains runtime health
LOGFILE="/opt/SELFIX/logs/maintenance.log"
echo "----------------------------------------" | tee -a "$LOGFILE"
echo "[🧹] SELFIX Runtime Cleanup Started at $(date)" | tee -a "$LOGFILE"

# === Step 1: Kill Duplicate Uvicorn Processes ===
UVICORN_PROCESSES=$(ps aux | grep uvicorn | grep -v grep)

while IFS= read -r line; do
    [ -z "$line" ] && continue

    if echo "$line" | grep -q "main_api:app"; then
        echo "[✅] Keeping main_api Uvicorn: $line" | tee -a "$LOGFILE"
    else
        PID=$(echo "$line" | awk '{print $2}')
        if [[ "$PID" =~ ^[0-9]+$ ]]; then
            echo "[💀] Killing duplicate Uvicorn PID: $PID" | tee -a "$LOGFILE"
            kill -9 "$PID"
        else
            echo "[⚠️] Skipped invalid PID: $PID" | tee -a "$LOGFILE"
        fi
    fi
done <<< "$UVICORN_PROCESSES"

# === Step 2: Remove Healing Trigger Files ===
rm -f /tmp/trigger_healing.txt && \
echo "[🧼] Removed /tmp/trigger_healing.txt" | tee -a "$LOGFILE"

# === Step 3: Clean Logs Older Than 30 Days ===
find /opt/SELFIX/logs -type f -mtime +30 -exec rm -f {} \; && \
echo "[🗑️] Deleted logs older than 30 days" | tee -a "$LOGFILE"

# === Step 4: Confirm and Exit ===
echo "[✅] Runtime cleanup complete." | tee -a "$LOGFILE"
echo "----------------------------------------" | tee -a "$LOGFILE"
