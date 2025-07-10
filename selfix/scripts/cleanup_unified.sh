#!/bin/bash
set -e

# ───────────────────────────────────────────────
# 🧹 SELFIX Commercial Cleanup Script
# Refactor structure, archive junk, prep for unified installer
# ───────────────────────────────────────────────

STAMP=$(date +%Y%m%d_%H%M%S)
LOGFILE="/opt/SELFIX/logs/cleanup_${STAMP}.log"
mkdir -p /opt/SELFIX/logs

log() {
  echo "[*] $1" | tee -a "$LOGFILE"
}

log "Starting cleanup process..."

# ─── 1. Remove duplicate or old files ───────────
log "Removing backup & temp files..."
find /opt/SELFIX -type f \( -name "*.bak" -o -name "*.old.py" -o -name "*~" \) -exec rm -v {} \; >> "$LOGFILE"

# ─── 2. Remove strange typos ─────────────────────
if [ -f "/opt/SELFIX/start_smart.shh" ]; then
  log "Removing typo: start_smart.shh"
  rm -f /opt/SELFIX/start_smart.shh
fi

# ─── 3. Archive nested SELFIX folder ─────────────
if [ -d "/opt/SELFIX/SELFIX" ]; then
  mkdir -p /opt/SELFIX/docs/legal
  mv /opt/SELFIX/SELFIX/*.pdf /opt/SELFIX/docs/legal/ 2>/dev/null || true
  mv /opt/SELFIX/SELFIX/README.md /opt/SELFIX/docs/legal/ 2>/dev/null || true
  mv /opt/SELFIX/SELFIX/test_sync.txt /opt/SELFIX/_archive/ 2>/dev/null || true
  rmdir /opt/SELFIX/SELFIX 2>/dev/null || true
  log "Nested SELFIX/ moved and removed."
fi

# ─── 4. Clean up quarantine folder ───────────────
log "Archiving any dangerous quarantine files..."
mkdir -p /opt/SELFIX/quarantine/archive
mv /opt/SELFIX/quarantine/*backdoor*.sh /opt/SELFIX/quarantine/archive/ 2>/dev/null || true

# ─── 5. Organize engine components ───────────────
log "Reorganizing scripts..."
mkdir -p /opt/SELFIX/engine
mkdir -p /opt/SELFIX/scripts/qc

mv /opt/SELFIX/healing_*.py /opt/SELFIX/engine/ 2>/dev/null || true
mv /opt/SELFIX/trap_logic.py /opt/SELFIX/engine/ 2>/dev/null || true
mv /opt/SELFIX/verify_engine.py /opt/SELFIX/engine/ 2>/dev/null || true
mv /opt/SELFIX/golden_vault_manager.py /opt/SELFIX/engine/ 2>/dev/null || true

# ─── 6. Remove generated temp folder ─────────────
if [ -d "/opt/SELFIX/generated" ]; then
  log "Archiving generated folder..."
  mkdir -p /opt/SELFIX/_archive/generated_${STAMP}
  mv /opt/SELFIX/generated/* /opt/SELFIX/_archive/generated_${STAMP}/ 2>/dev/null || true
  rmdir /opt/SELFIX/generated 2>/dev/null || true
fi

# ─── 7. Consolidate backups folder ───────────────
if compgen -G "/opt/SELFIX/backups/*.bak" > /dev/null; then
  log "Archiving .bak backups..."
  tar czf /opt/SELFIX/_archive/backups_${STAMP}.tar.gz /opt/SELFIX/backups/*.bak
  rm -f /opt/SELFIX/backups/*.bak
fi

# ─── 8. Normalize node_modules (optional) ────────
if [ -d "/opt/SELFIX/node_modules" ] && [ -d "/opt/SELFIX/stripe-server/node_modules" ]; then
  log "Both node_modules directories exist. Keeping both."
fi

# ─── 9. Log complete ─────────────────────────────
log "Cleanup complete. Log saved to: $LOGFILE"
