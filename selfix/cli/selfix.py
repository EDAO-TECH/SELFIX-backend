#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# === ✅ Dynamic path resolution for USB or VPS installs ===
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

# === 🔧 SELFIX imports ===
from selfix.engine.book_of_forgiveness import seal_file, verify_all, restore_file
from selfix.core.env import PATHS

# === 📜 Forgiveness logging path ===
FORGIVENESS_LOG = os.path.join(PATHS["LOG"], "forgiveness_history.log")

def log_forgive_event(file_path):
    os.makedirs(os.path.dirname(FORGIVENESS_LOG), exist_ok=True)
    with open(FORGIVENESS_LOG, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] SEALED via CLI: {file_path}\n")

def print_help():
    print("""
🔧 SELFIX CLI Tool — Self-Healing Infrastructure eXtension

Usage:
  selfix check                     → Run system precheck
  selfix report                    → Show last 3 reports
  selfix status                    → Show agent/service/system status
  selfix trap                      → Trigger Trap Logic™
  selfix rollback <component>     → Restore a component from backup
  selfix license                   → Check SmartLicense-X™ status
  selfix audit                     → Generate compliance report
  selfix qc <module>               → Run quality check on healing module
  selfix vault promote <module>   → Promote QC-passed module to vault
  selfix vault export              → Export all vault contents (.tar.gz)
  selfix heal                      → Run global healing
  selfix fix <component>           → Targeted healing for one component
  selfix doc                       → Generate /opt/SELFIX/SERVICES.md
  selfix services                  → Show unit/service/module status
  selfix about                     → Show brand + mission

  selfix forgive --seal <file>     → Seal file into Book of Forgiveness
  selfix forgive --verify          → Verify integrity of sealed files
  selfix forgive --restore <file>  → Restore trusted file from Book of Forgiveness
  selfix help                      → Show this help
""")

def main():
    args = sys.argv[1:]

    if not args or args[0] in ("help", "--help", "-h"):
        print_help()
        return

    cmd = args[0]

    # === CORE ===
    if cmd == "check":
        os.system(f"python3 {ROOT}/selfix/scripts/selfix_precheck.py")

    elif cmd == "report":
        os.system(f"tail -n 30 {ROOT}/forgiveness/reports/verify_*.log | less")

    elif cmd == "status":
        os.system("systemctl list-units | grep selfix")

    elif cmd == "trap":
        os.system(f"python3 {ROOT}/selfix/engine/trap_logic.py")

    elif cmd == "rollback" and len(args) > 1:
        os.system(f"python3 {ROOT}/selfix/scripts/rollback.py {args[1]}")

    elif cmd == "license":
        os.system(f"cat {ROOT}/selfix/configs/selfix_license.key")

    elif cmd == "audit":
        os.system(f"python3 {ROOT}/selfix/scripts/compliance_report.py")

    elif cmd == "qc" and len(args) > 1:
        os.system(f"python3 {ROOT}/selfix/scripts/qc_module.py {args[1]}")

    elif cmd == "vault":
        if len(args) > 2 and args[1] == "promote":
            os.system(f"python3 {ROOT}/selfix/scripts/promote_to_vault.py {args[2]}")
        elif len(args) > 1 and args[1] == "export":
            os.system(f"tar czf {ROOT}/vault_export.tar.gz {ROOT}/book_of_forgiveness/vault/")

    elif cmd == "heal":
        os.system(f"python3 {ROOT}/selfix/scripts/selfix_heal.py")

    elif cmd == "fix" and len(args) > 1:
        os.system(f"python3 {ROOT}/selfix/scripts/selfix_target_heal.py {args[1]}")

    elif cmd == "doc":
        os.system(f"python3 {ROOT}/selfix/scripts/generate_service_doc.py")

    elif cmd == "services":
        os.system(f"python3 {ROOT}/selfix/scripts/show_services.py")

    elif cmd == "about":
        print("""
🔧 SELFIX — Self-Healing Infrastructure eXtension
🔐 Built by Nevermissed • Licensed by SmartLicense-X™

✅ Autonomous healing engine
✅ Sealed with Book of Forgiveness
✅ Logs, restores, and protects your infrastructure

📍 For support, visit /opt/SELFIX/docs or contact HQ
""")

    # === BOOK OF FORGIVENESS ===
    elif cmd == "forgive":
        subcmd = args[1] if len(args) > 1 else None
        if subcmd == "--seal" and len(args) > 2:
            seal_file(args[2])
            log_forgive_event(args[2])
        elif subcmd == "--verify":
            verify_all()
        elif subcmd == "--restore" and len(args) > 2:
            restore_file(args[2])
        else:
            print("""
Usage:
  selfix forgive --seal <file>      → Seal and QC a trusted file
  selfix forgive --verify           → Verify integrity of all sealed files
  selfix forgive --restore <file>   → Restore a trusted version from seal
""")

    else:
        print(f"❌ Unknown command: {cmd}")
        print_help()

if __name__ == "__main__":
    main()
