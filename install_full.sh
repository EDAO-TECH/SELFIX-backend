#!/bin/bash

set -e
echo ""
echo "🚀 SELFIX Full Installer (Commercial Edition)"
echo "─────────────────────────────────────────────"

# ─── 1. RUN PRECHECK ─────────────────────────────
echo "🔎 Running pre-install system check..."
python3 /opt/SELFIX/scripts/selfix_precheck.py || {
  echo "❌ Precheck failed. Aborting installation."
  exit 1
}

# ─── 2. PYTHON ENV SETUP ─────────────────────────
echo "🐍 Setting up Python environment..."
if [ ! -d "/opt/SELFIX/venv" ]; then
  python3 -m venv /opt/SELFIX/venv
fi
source /opt/SELFIX/venv/bin/activate
pip install --upgrade pip
pip install -r /opt/SELFIX/requirements.txt

# ─── 3. NODE MODULES ─────────────────────────────
if [ -f "/opt/SELFIX/package.json" ]; then
  echo "📦 Installing Node.js modules..."
  cd /opt/SELFIX && npm install
fi

# ─── 4. ENABLE SERVICES ──────────────────────────
echo "🛠️ Registering system services..."
cp /opt/SELFIX/selfix.service /etc/systemd/system/selfix.service
systemctl daemon-reload
systemctl enable selfix

# Optional future services:
# cp selfix-chat.service /etc/systemd/system/
# cp selfix-seeder.service /etc/systemd/system/
# systemctl enable selfix-chat selfix-seeder

# ─── 5. START SELFIX ─────────────────────────────
echo "🚀 Starting SELFIX..."
systemctl start selfix

# ─── 6. FINISH ───────────────────────────────────
echo ""
echo "🎉 SELFIX installation complete."
echo "📍 Location: /opt/SELFIX"
echo "🧪 Run precheck: selfix-precheck"
echo "💬 Start local AI: selfix-chat (if installed)"
echo "📡 Seeder agent: selfix-seeder (if installed)"
echo ""
