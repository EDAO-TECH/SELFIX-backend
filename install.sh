#!/bin/bash

set -e
set -o pipefail

echo ""
echo "🛡️  Installing SELFIX CyberDefense Stack (Commercial Edition)"
echo "=============================================================="

# ---[ 1. SYSTEM CHECKS ]---
echo "🔍 Checking system requirements..."

PYTHON=$(which python3)
VERSION=$($PYTHON -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$VERSION" < "3.10" ]]; then
  echo "❌ Python 3.10+ is required. Found $VERSION"
  exit 1
fi

# Required OS packages
echo "📦 Installing system dependencies..."
sudo apt update -y
sudo apt install -y build-essential libreadline-dev libncurses5-dev libncursesw5-dev curl git

# ---[ 2. PYTHON ENVIRONMENT ]---
echo "🐍 Setting up Python virtual environment..."
cd /opt/SELFIX

if [[ -d "venv" ]]; then
  echo "🧪 Using existing virtual environment..."
  source venv/bin/activate
elif command -v python3 -m venv &> /dev/null; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
  source venv/bin/activate
else
  echo "⚠️ virtualenv not available. Continuing with system Python..."
fi

echo "⬆️  Upgrading pip and installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r /opt/SELFIX/requirements.txt

# ---[ 2b. NODE.JS DEPENDENCIES ]---
echo "🧩 Installing Node.js packages (for frontend/unified)..."
if [ -f "package.json" ]; then
  npm install --silent || echo "⚠️ npm install failed (check node setup)"
else
  echo "⚠️ Skipping npm install — package.json not found."
fi

# ---[ 3. LICENSE ENFORCEMENT ]---
echo "🔐 Verifying SELFIX commercial license..."

LICENSE_DIR="/opt/SELFIX/config"
LICENSE_FILE="${LICENSE_DIR}/selfix_license.key"
mkdir -p "$LICENSE_DIR"

if [[ ! -f "$LICENSE_FILE" ]]; then
  echo "⚠️ No license key found."
  read -p "🔑 Enter your SELFIX license key: " LICENSE_KEY
  echo "$LICENSE_KEY" > "$LICENSE_FILE"
  echo "✅ License key saved to $LICENSE_FILE"
else
  echo "✅ License key already exists."
fi

# ---[ 4. DATA DIRECTORIES ]---
echo "📁 Creating SELFIX runtime folders..."
mkdir -p /opt/SELFIX/logs /opt/SELFIX/reports /opt/SELFIX/data /opt/SELFIX/licenses

# ---[ 5. PERMISSIONS & EXECUTABLES ]---
echo "🔐 Setting script permissions..."
chmod +x /opt/SELFIX/start_all.sh
chmod +x /opt/SELFIX/scripts/*.py 2>/dev/null || true

# ---[ 6. GLOBAL CLI SHORTCUTS ]---
echo "🔗 Linking CLI tools system-wide..."
ln -sf /opt/SELFIX/scripts/selfix_precheck.py /usr/local/bin/selfix
ln -sf /opt/SELFIX/scripts/selfix_chat.py     /usr/local/bin/selfix-chat
# Optional additional tools
# ln -sf /opt/SELFIX/scripts/selfix_status.py /usr/local/bin/selfix-status

# ---[ 7. LAUNCH BACKEND + SERVICES ]---
echo "🚀 Starting SELFIX stack..."
/opt/SELFIX/start_all.sh

# ---[ 8. RUN PRECHECK ]---
echo "🧪 Running system integrity check..."
if selfix precheck > /dev/null; then
  echo "✅ Precheck passed."
else
  echo "⚠️  Precheck warnings found. Check /opt/SELFIX/reports/"
fi

# ---[ 9. SYSTEMD INTEGRATION (OPTIONAL) ]---
if command -v systemctl &> /dev/null; then
  echo ""
  echo "🛠️  To enable SELFIX to start on boot:"
  echo "   sudo cp /opt/SELFIX/selfix.service /etc/systemd/system/"
  echo "   sudo systemctl enable selfix && sudo systemctl start selfix"
fi

# ---[ 10. DONE ]---
echo ""
echo "🎉 SELFIX Commercial Installation Complete!"
echo "📍 Installed in:      /opt/SELFIX"
echo "🧪 Run precheck:      selfix"
echo "💬 Start chat:        selfix-chat"
echo "📜 Logs:              tail -f /opt/SELFIX/logs/healing_loop.log"
echo ""
