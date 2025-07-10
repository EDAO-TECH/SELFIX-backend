#!/bin/bash

set -e
set -o pipefail

echo ""
echo "🗑️  SELFIX UNINSTALLER"
echo "=============================="

read -p "⚠️  Are you sure you want to uninstall SELFIX? [y/N]: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "❌ Uninstall cancelled."
  exit 0
fi

# ---[ 1. Stop any running services ]---
echo "🛑 Stopping SELFIX services (if any)..."
if systemctl is-active --quiet selfix; then
  sudo systemctl stop selfix
  sudo systemctl disable selfix
  sudo rm -f /etc/systemd/system/selfix.service
fi

# ---[ 2. Remove CLI symlinks ]---
echo "🧹 Removing global CLI commands..."
rm -f /usr/local/bin/selfix
rm -f /usr/local/bin/selfix-chat
rm -f /usr/local/bin/selfix-status

# ---[ 3. Remove SELFIX directory ]---
echo "🧨 Deleting /opt/SELFIX/ directory..."
rm -rf /opt/SELFIX/

# ---[ 4. Clean Python venv (optional) ]---
# Uncomment if you want to remove Python venvs outside /opt/SELFIX

# ---[ 5. Final message ]---
echo ""
echo "✅ SELFIX has been completely uninstalled."
echo ""
