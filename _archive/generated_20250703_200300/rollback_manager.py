import shutil
import json
from pathlib import Path
from datetime import datetime

MODULES_DIR = Path("/opt/SELFIX/healing_modules/promoted")
BACKUP_DIR = Path("/opt/SELFIX/backups")
LOG_FILE = Path("/opt/SELFIX/data/rollback_log.json")

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def backup_module(module_file):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"{module_file.stem}_{timestamp}.bak"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy(module_file, backup_path)
    return backup_path

def rollback_latest(module_name):
    backups = sorted(BACKUP_DIR.glob(f"{module_name}_*.bak"), reverse=True)
    if not backups:
        print(f"⚠️ No backups found for {module_name}")
        return None
    latest_backup = backups[0]
    target_path = MODULES_DIR / f"{module_name}.py"
    shutil.copy(latest_backup, target_path)
    return str(latest_backup)

def log_action(module, backup):
    if LOG_FILE.exists():
        log = json.loads(LOG_FILE.read_text())
    else:
        log = []
    log.append({
        "timestamp": datetime.now().isoformat(),
        "module": module,
        "restored_from": backup
    })
    LOG_FILE.write_text(json.dumps(log, indent=2))

def main():
    example_module = "entropy_fix_cpu"
    module_file = MODULES_DIR / f"{example_module}.py"

    if module_file.exists():
        backup = backup_module(module_file)
        print(f"📦 Backed up {module_file.name} → {backup}")
        restored = rollback_latest(example_module)
        if restored:
            log_action(example_module, restored)
            print(f"✅ Rolled back {example_module} from {restored}")
    else:
        print("⚠️ Module not found. Nothing to backup or restore.")

if __name__ == "__main__":
    main()
