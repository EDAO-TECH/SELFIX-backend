import os
import subprocess
from selfix.core.env import PATHS
from selfix.engine import hmac_utils

# === CONFIG ===
FORGIVEN_BY = "TENG ZHI LI"
REASON = "healing module"
FILES_TO_SEAL = [
    "selfix/engine/healing_manager.py",
    "selfix/scripts/selfix_heal.py",
    "selfix/configs/ai_policy.json",
    "selfix/plugins/plugin_custom_responder.py"
]

# === UTILS ===
def seal(file_path):
    cmd = [
        "python3",
        "selfix/cli/selfix.py",
        "forgive",
        "--seal",
        file_path
    ]
    env = os.environ.copy()
    env["FORGIVEN_BY"] = FORGIVEN_BY
    env["SEAL_REASON"] = REASON

    print(f"🔒 Sealing {file_path}...")
    result = subprocess.run(cmd, env=env)
    if result.returncode == 0:
        print(f"✅ Sealed: {file_path}")
    else:
        print(f"❌ Failed: {file_path}")

# === MAIN ===
print(f"\n📍 Detected ROOT: {PATHS['ROOT']}")
print("📜 Starting full seal sequence...\n")

for path in FILES_TO_SEAL:
    seal(path)

# === SIGN MANIFEST ===
print("\n🔏 Signing updated manifest...")
hmac_utils.sign_manifest(
    PATHS["MANIFEST"],
    PATHS["SIGNATURE"],
    PATHS["SECRET_KEY"]
)
print("✅ Manifest signed.")

print("\n🎉 All files sealed and manifest signed.")
