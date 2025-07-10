#!/bin/bash

echo "🔍 Running SELFIX post-upgrade verification..."

# Check critical services
echo -e "\n🛡️ Service status:"
systemctl is-active selfix-agent
systemctl is-active nginx
systemctl is-active ssh

# Show last events
echo -e "\n📜 Last 10 healing logs:"
tail -n 10 /opt/SELFIX/logs/healing_daemon.log

# Run internal status check
echo -e "\n🔧 Running defender status:"
python3 /opt/SELFIX/scripts/defender_status.py

echo -e "\n✅ Post-upgrade checks complete."
