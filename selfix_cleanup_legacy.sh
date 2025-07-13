#!/bin/bash

echo "🧹 Cleaning up obsolete SELFIX files..."

cd /opt/SELFIX || exit 1

# Remove old scripts
rm -v start_all.sh install.sh final_install_backup.sh selfix_precheck.py 2>/dev/null

# Remove unsafe .env files
rm -v .env .env.save .env.save.1 2>/dev/null

# Confirm
echo "✅ Cleanup complete. Legacy files removed:"
ls -1 | grep -E 'start_all|install|precheck|.env'

echo "📁 Now using:"
echo " - selfix_smart_install.sh"
echo " - selfix_smart_precheck.py"
echo " - selfix_smart_start.sh"
echo " - selfix_smart_service_setup.sh"
