#!/bin/bash

echo "🔄 [SELFIX] Starting auto-pull..."
cd /opt/SELFIX || exit 1

# Optional backup before update
cp -r /opt/SELFIX /opt/SELFIX_backup_$(date +"%Y%m%d_%H%M")

# Pull latest repo changes
if git pull origin main; then
    echo "✅ [SELFIX] Update pulled successfully."
else
    echo "❌ [SELFIX] Git pull failed. Check internet or repo access."
    exit 2
fi

# Optional: Restart core services
if pgrep -f healing_daemon.py; then
    pkill -f healing_daemon.py
fi
nohup python3 /opt/SELFIX/healing_daemon.py >> /opt/SELFIX/logs/healing_loop.log 2>&1 &

echo "🎉 [SELFIX] Auto-pull complete. Healing Daemon restarted."
