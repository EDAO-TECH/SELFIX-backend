#!/bin/bash

echo "🔧 Starting SELFIX Unified Installer"
echo "======================================"

# Default base path
BASE_DIR="/opt/SELFIX"
SERVICE_LIST=("selfix-agent" "selfix-av" "selfix-seeder" "selfix-hq" "selfix-backend" "selfix-core" "selfix-api" "selfix-labs" "selfix-monitor" "selfix_webhook")

# Optional: Ask user to select which services to enable
echo "🧩 Available services:"
for i in "${!SERVICE_LIST[@]}"; do
  echo "  $((i+1)). ${SERVICE_LIST[$i]}"
done

echo -n "Enter service numbers to enable (e.g. 1 3 5): "
read -a SELECTED_INDEXES

SELECTED_SERVICES=()
for i in "${SELECTED_INDEXES[@]}"; do
  SELECTED_SERVICES+=("${SERVICE_LIST[$((i-1))]}")
done

echo "✅ Selected services: ${SELECTED_SERVICES[@]}"

# Ensure systemd is present
if ! command -v systemctl &> /dev/null; then
  echo "❌ systemctl not found. Exiting."
  exit 1
fi

echo "🔄 Installing selected services..."
for SERVICE in "${SELECTED_SERVICES[@]}"; do
  SERVICE_FILE="/etc/systemd/system/${SERVICE}.service"
  
  if [ -f "$SERVICE_FILE" ]; then
    echo "🔁 Enabling and starting: $SERVICE"
    systemctl enable "$SERVICE"
    systemctl restart "$SERVICE"
  else
    echo "⚠️  Service file not found: $SERVICE_FILE"
  fi
done

# Optional symlinks or CLI entry points
echo "🔗 Creating CLI entry..."
ln -sf "$BASE_DIR/scripts/selfix_precheck.py" /usr/local/bin/selfix 2>/dev/null
chmod +x /usr/local/bin/selfix

echo "✅ Unified install complete."
