#!/usr/bin/env python3
"""
SELFIX Command-Line Interface
-----------------------------
Usage:
    python3 selfix_tools.py cleanup --type runtime
    python3 selfix_tools.py audit
"""

import argparse
import subprocess
import os
from pathlib import Path

def run_cleanup(script_path, mode="python"):
    if mode == "python":
        subprocess.run(["python3", script_path])
    elif mode == "bash":
        subprocess.run(["bash", script_path])

def run_audit():
    print("📊 SELFIX System Audit\n----------------------------")
    base = Path.cwd()

    # Count all files and directories
    num_files = sum(1 for _ in base.rglob("*") if _.is_file())
    num_dirs = sum(1 for _ in base.rglob("*") if _.is_dir())
    print(f"[📁] Total files: {num_files}")
    print(f"[📂] Total directories: {num_dirs}")

    # Count .bak files
    bak_files = list(base.rglob("*.bak"))
    print(f"[🗑️] .bak files found: {len(bak_files)}")
    if bak_files:
        print("   Examples:")
        for f in bak_files[:3]:
            print(f"     - {f}")

    # Check for empty folders
    empty_dirs = [p for p in base.rglob("*") if p.is_dir() and not any(p.iterdir())]
    print(f"[🚫] Empty folders: {len(empty_dirs)}")

    # Log folder size
    log_dir = base / "logs"
    if log_dir.exists():
        total_log_size = sum(f.stat().st_size for f in log_dir.rglob("*") if f.is_file())
        print(f"[📜] Log folder size: {total_log_size / 1024:.2f} KB")
    else:
        print("[📜] Log folder not found.")

    # Count promoted healing modules
    promoted_dir = base / "healing_modules/promoted"
    if promoted_dir.exists():
        promoted_count = len(list(promoted_dir.glob("*.py")))
        print(f"[🛡️] Promoted healing modules: {promoted_count}")
    else:
        print("[🛡️] No promoted modules directory found.")

    print("----------------------------\n✅ Audit complete.")

def main():
    parser = argparse.ArgumentParser(description="SELFIX Toolkit CLI")
    sub = parser.add_subparsers(dest="command")

    # cleanup command
    cleanup_cmd = sub.add_parser("cleanup", help="Run cleanup routines")
    cleanup_cmd.add_argument(
        "--type",
        choices=["dev", "runtime", "vault", "filename"],
        required=True,
        help="Choose which type of cleanup to run"
    )

    # audit command
    audit_cmd = sub.add_parser("audit", help="Run SELFIX audit diagnostics")

    args = parser.parse_args()

    if args.command == "cleanup":
        match args.type:
            case "dev":
                run_cleanup("scripts/cleanup/selfix_cleanup.py")
            case "runtime":
                run_cleanup("scripts/cleanup/selfix_runtime_cleanup.sh", mode="bash")
            case "vault":
                run_cleanup("scripts/vault/cleanup_staging.py")
            case "filename":
                run_cleanup("selfix_tools/filename_cleaner.py")
            case _:
                print("❌ Unknown cleanup type")
    elif args.command == "audit":
        run_audit()

if __name__ == "__main__":
    main()
