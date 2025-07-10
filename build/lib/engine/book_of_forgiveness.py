# /opt/SELFIX/engine/book_of_forgiveness.py

import os, shutil, hashlib, json, subprocess
from datetime import datetime

FORGIVENESS_DIR = "/opt/SELFIX/forgiveness"
FILES_DIR = os.path.join(FORGIVENESS_DIR, "files")
META_DIR = os.path.join(FORGIVENESS_DIR, "meta")
MANIFEST_PATH = os.path.join(META_DIR, "manifest.json")
LOG_PATH = os.path.join(FORGIVENESS_DIR, "logs/forgiveness_history.log")

os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def _log(msg):
    timestamp = datetime.now().isoformat()
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def _hash_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def _load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r') as f:
            return json.load(f)
    return {}

def _save_manifest(data):
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def seal_file(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return

    filename = os.path.basename(path)

    print(f"🧪 QC: Executing {filename} for test...")
    try:
        subprocess.run(["python3", path], check=True, timeout=10)
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        _log(f"QC FAILED: {filename} — {e}")
        return

    dest_path = os.path.join(FILES_DIR, filename)
    shutil.copy2(path, dest_path)
    file_hash = _hash_file(dest_path)

    manifest = _load_manifest()
    manifest[filename] = {
        "original_path": path,
        "hash": file_hash,
        "qc_passed": True,
        "timestamp": datetime.now().isoformat()
    }
    _save_manifest(manifest)
    _log(f"SEALED: {filename} (SHA256: {file_hash})")
    print(f"✅ File sealed successfully.")

def verify_all():
    manifest = _load_manifest()
    for filename, meta in manifest.items():
        path = meta["original_path"]
        if not os.path.exists(path):
            print(f"⚠️ Missing file: {path}")
            continue
        current_hash = _hash_file(path)
        if current_hash != meta["hash"]:
            print(f"❌ {filename}: HASH MISMATCH")
            _log(f"TAMPER DETECTED: {filename}")
        else:
            print(f"✅ {filename}: OK")

def restore_file(filename):
    manifest = _load_manifest()
    if filename not in manifest:
        print(f"❌ No such file in forgiveness record: {filename}")
        return

    src = os.path.join(FILES_DIR, filename)
    dst = manifest[filename]["original_path"]
    shutil.copy2(src, dst)
    _log(f"RESTORED: {filename} → {dst}")
    print(f"✅ Restored: {filename}")
