#!/usr/bin/env python3

import os
import json
import datetime
import argparse
import importlib.util
import threading
import time
from pathlib import Path

REPORT_PATH = "/opt/SELFIX/reports"

# Dynamically load a module from a path
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def check_status_registry(health_data):
    try:
        with open("data/status_registry.yaml", "r") as f:
            lines = f.readlines()
            health_data["components"]["system_status"] = "OK" if lines else "Empty"
    except Exception as e:
        health_data["components"]["system_status"] = f"ERROR: {str(e)}"

def check_vault(health_data):
    try:
        vault_checker = load_module("vault_checker", "/opt/SELFIX/scripts/check_vault_integrity.py")
        vault_checker.main()
        health_data["components"]["vault_integrity"] = "OK"
    except Exception as e:
        health_data["components"]["vault_integrity"] = f"ERROR: {str(e)}"

def check_karma(health_data):
    try:
        karma_tester = load_module("karma_tester", "/opt/SELFIX/scripts/karma_tester.py")
        result = karma_tester.run_karma_check()
        health_data["components"]["karma_check"] = result
    except Exception as e:
        health_data["components"]["karma_check"] = f"ERROR: {str(e)}"

def check_healing_verifier(health_data):
    try:
        healing_verifier = load_module("healing_verifier", "/opt/SELFIX/generated/healing_verifier.py")
        result = healing_verifier.run_verifier()
        health_data["components"]["healing_verification"] = result
    except Exception as e:
        health_data["components"]["healing_verification"] = f"ERROR: {str(e)}"

def summarize_logs(health_data):
    try:
        with open("logs/healing_loop.log", "r") as f:
            lines = f.readlines()[-10:]
            health_data["components"]["recent_healing_logs"] = lines
    except:
        health_data["components"]["recent_healing_logs"] = "Log not found"

def generate_report(health_data):
    report_file = f"precheck_report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    os.makedirs(REPORT_PATH, exist_ok=True)
    with open(os.path.join(REPORT_PATH, report_file), "w") as f:
        json.dump(health_data, f, indent=4)
    print(f"✔️ Report saved to: {os.path.join(REPORT_PATH, report_file)}")

def run_precheck():
    health_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "components": {},
        "summary": ""
    }
    print("🛡️  Running SELFIX Pre-Health Check...")
    check_status_registry(health_data)
    check_vault(health_data)
    check_karma(health_data)
    check_healing_verifier(health_data)
    summarize_logs(health_data)
    generate_report(health_data)

def run_doctor():
    print("👨‍⚕️ Welcome to SELFIX Doctor Mode (type 'exit' to quit)")
    while True:
        try:
            question = input("[You]: ")
            if question.lower() in ["exit", "quit"]:
                print("👋 Exiting doctor mode.")
                break
            else:
                ai_module = load_module("local_ai", "/opt/SELFIX/local_ai.py")
                response = ai_module.ask_local_ai(question)
                print(f"[Local AI]: {response}")
        except Exception as e:
            print(f"[Error]: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="SELFIX CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("precheck", help="Run the SELFIX Pre-Health Check")
    subparsers.add_parser("doctor", help="Talk to the SELFIX Local AI about system health")

    args = parser.parse_args()

    if args.command == "precheck":
        run_precheck()
    elif args.command == "doctor":
        run_doctor()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
