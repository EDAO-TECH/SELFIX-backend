import hashlib
from pathlib import Path
import json
from datetime import datetime

PROMOTED_DIR = Path("/opt/SELFIX/healing_modules/promoted")
OUTPUT = Path("/opt/SELFIX/data/healing_verifier_log.json")

def hash_file(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    log = []
    if not PROMOTED_DIR.exists():
        print(f"⚠️ PROMOTED_DIR does not exist: {PROMOTED_DIR}")
        return

    for pyfile in PROMOTED_DIR.glob("*.py"):
        stat = pyfile.stat()
        created = datetime.fromtimestamp(stat.st_ctime).isoformat()
        sha256 = hash_file(pyfile)
        log.append({
            "filename": pyfile.name,
            "sha256": sha256,
            "created": created
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(log, indent=2))
    print(f"✅ healing_verifier completed. Results in {OUTPUT}")

if __name__ == "__main__":
    main()
