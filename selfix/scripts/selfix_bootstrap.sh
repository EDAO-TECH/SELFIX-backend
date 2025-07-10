#!/bin/bash

# ────────────────────────────────────────────────
# 🧪 STEP 1: Run Full System Precheck
# ────────────────────────────────────────────────
echo "🧪 Running SELFIX Precheck..."
PRECHECK_SCRIPT="/opt/SELFIX/scripts/selfix_precheck.py"
if [ ! -f "$PRECHECK_SCRIPT" ]; then
    echo "❌ Precheck script not found at $PRECHECK_SCRIPT"
    exit 1
fi

python3 "$PRECHECK_SCRIPT"

# ────────────────────────────────────────────────
# 🛠️ STEP 2: Interactive Service Setup
# ────────────────────────────────────────────────
echo ""
echo "🛠️ Starting SELFIX Unified Installer"
echo "========================================"

BASE_DIR="/opt/SELFIX"
SERVICE_LIST=("selfix-agent" "selfix-av" "selfix-seeder" "selfix-hq" "selfix-backend" "selfix-core" "selfix-api" "selfix-labs" "selfix-monitor" "selfix_webhook")

# Display services
echo "🧩 Available services:"
for i in "${!SERVICE_LIST[@]}"; do
  echo "  $((i+1)). ${SERVICE_LIST[$i]}"
done

# Prompt for selection
read -p "Enter service numbers to enable (e.g. 1 3 5): " -a SELECTED_INDEXES

# Build list of selected services
SELECTED_SERVICES=()
for i in "${SELECTED_INDEXES[@]}"; do
  SELECTED_SERVICES+=("${SERVICE_LIST[$((i-1))]}")
done

echo "✅ Selected services: ${SELECTED_SERVICES[@]}"

# Ensure systemctl available
if ! command -v systemctl &> /dev/null; then
  echo "❌ systemctl not found. Are you on a minimal system?"
  exit 1
fi

# Enable + restart services
echo "🔄 Enabling selected services..."
for SERVICE in "${SELECTED_SERVICES[@]}"; do
  SERVICE_FILE="/etc/systemd/system/${SERVICE}.service"
  
  if [ -f "$SERVICE_FILE" ]; then
    echo "🔁 Enabling + restarting: $SERVICE"
    systemctl enable "$SERVICE"
    systemctl restart "$SERVICE"
  else
    echo "⚠️  Skipping: $SERVICE_FILE not found"
  fi
done

# CLI shortcut
echo "🔗 Linking CLI tools..."
ln -sf "$PRECHECK_SCRIPT" /usr/local/bin/selfix
chmod +x /usr/local/bin/selfix

echo ""
echo "✅ Bootstrap complete! Run 'selfix' anytime to recheck."
