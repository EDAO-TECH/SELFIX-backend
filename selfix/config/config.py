# Filename: selfix/config/config.py

"""
config.py

Contains centralized configuration paths and constants
for the SELFIX Book of Forgiveness system.
"""

from pathlib import Path

# Base directory for SELFIX deployment
BASE_DIR = Path("/opt/SELFIX")

# Book of Forgiveness root directory
FORGIVENESS_DIR = BASE_DIR / "forgiveness"

# Where sealed copies of files are stored (read-only vault)
SEALED_DIR = FORGIVENESS_DIR / "files"

# Manifest location (contains sealing metadata)
MANIFEST_PATH = FORGIVENESS_DIR / "meta" / "manifest.json"

# Log location (JSONL structured logs)
FORGIVENESS_LOG_PATH = FORGIVENESS_DIR / "logs" / "forgiveness_history.log"

# Customer-defined file list for sealing (Tier 2)
TARGET_LIST_PATH = BASE_DIR / "conf" / "forgiveness_targets.txt"

# Tier 1 — Core SELFIX healing logic files to auto-seal
CRITICAL_FILES = [
    "/opt/SELFIX/selfix/engine/healing_manager.py",
    "/opt/SELFIX/selfix/scripts/selfix_heal.py",
    "/opt/SELFIX/selfix/scripts/selfix_precheck.py",
    "/opt/SELFIX/selfix/cli/selfix.py",
    "/opt/SELFIX/selfix/configs/ai_policy.json",
]

# Optional: Standard metadata fields for manifest entries
SEAL_META_FIELDS = [
    "original_path",
    "sealed_path",
    "hash",
    "alias",
    "forgiven_by",
    "reason",
    "timestamp",
    "executable_valid",
]
