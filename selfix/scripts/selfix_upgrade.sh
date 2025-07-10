#!/bin/bash

LOG_FILE="/opt/SELFIX/logs/upgrade_$(date '+%Y%m%d_%H%M%S').log"
touch "$LOG_FILE"

echo "🧠 [SELFIX UPGRADE SCRIPT]" | tee -a "$LOG_FILE"
echo "⏱️  Started at: $(date)" | tee -a "$LOG_FILE"
echo "--------------------------------------------------" | tee -a "$LOG_FILE"

# Step 1: Update package list
echo "📦 Updating apt package list..." | tee -a "$LOG_FILE"
apt update >> "$LOG_FILE" 2>&1

# Step 2: Upgrade all packages with new config files automatically accepted
echo "⬆️  Upgrading all packages..." | tee -a "$LOG_FILE"
DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confnew" upgrade -y >> "$LOG_FILE" 2>&1

# Step 3: Restart key services
echo "🔁 Restarting SELFIX services..." | tee -a "$LOG_FILE"
systemctl restart selfix-agent.service >> "$LOG_FILE" 2>&1
systemctl restart nginx >> "$LOG_FILE" 2>&1
systemctl restart ssh >> "$LOG_FILE" 2>&1

# Step 4: Optional — Clean up unused packages (safe mode)
echo "🧹 Cleaning unused packages..." | tee -a "$LOG_FILE"
apt-get autoremove -y >> "$LOG_FILE" 2>&1
apt-get autoclean -y >> "$LOG_FILE" 2>&1

# Step 5: Run SELFIX status check
echo "🔍 Running defender status check..." | tee -a "$LOG_FILE"
python3 /opt/SELFIX/scripts/defender_status.py >> "$LOG_FILE" 2>&1

# Step 6: Final confirmation
echo "✅ Upgrade completed. Healing Daemon log tail:" | tee -a "$LOG_FILE"
tail -n 10 /opt/SELFIX/logs/healing_daemon.log | tee -a "$LOG_FILE"

echo "--------------------------------------------------" | tee -a "$LOG_FILE"
echo "🏁 Finished at: $(date)" | tee -a "$LOG_FILE"
