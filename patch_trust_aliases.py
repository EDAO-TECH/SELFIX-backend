import os
import json
import shutil

# === SETTINGS ===
book_path = "selfix/engine/book_of_forgiveness.py"
alias_path = "selfix/configs/seal_aliases.json"
backup_path = book_path + ".bak"

# === 1. Write seal_aliases.json ===
os.makedirs(os.path.dirname(alias_path), exist_ok=True)

aliases = {
    "forgiven_by": [
        "FOUNDER TENG ZHI LI",
        "TENG ZHI LI",
        "Teng Zhi Li"
    ],
    "reason": [
        "HEALING MODULE",
        "healing module",
        "Healing Module"
    ]
}

with open(alias_path, "w") as f:
    json.dump(aliases, f, indent=2)

print(f"✅ Created: {alias_path}")

# === 2. Patch book_of_forgiveness.py ===
if not os.path.exists(book_path):
    print(f"❌ Error: {book_path} not found")
    exit(1)

# Backup original
shutil.copyfile(book_path, backup_path)
print(f"🔒 Backup created: {backup_path}")

with open(book_path, "r") as f:
    lines = f.readlines()

# Insert logic after imports
insert_index = 0
for i, line in enumerate(lines):
    if line.strip().startswith("import"):
        insert_index = i + 1

patch_code = '''
import json
import os

alias_file = os.path.join("selfix", "configs", "seal_aliases.json")
if os.path.exists(alias_file):
    with open(alias_file) as f:
        SEAL_ALIASES = json.load(f)
else:
    SEAL_ALIASES = {
        "forgiven_by": ["FOUNDER TENG ZHI LI"],
        "reason": ["HEALING MODULE"]
    }

def is_trusted_entry(entry):
    forgiven_by_ok = entry.get("forgiven_by", "").strip() in SEAL_ALIASES["forgiven_by"]
    reason_ok = entry.get("reason", "").strip() in SEAL_ALIASES["reason"]
    return forgiven_by_ok and reason_ok
'''.strip("\n") + "\n"

lines.insert(insert_index, patch_code)

# Replace old check if it exists
patched_lines = []
replaced = False
for line in lines:
    if '"forgiven_by"' in line and '==' in line and not replaced:
        patched_lines.append("    if is_trusted_entry(entry):\n")
        replaced = True
    else:
        patched_lines.append(line)

with open(book_path, "w") as f:
    f.writelines(patched_lines)

print(f"✅ Patched: {book_path}")
print("🎉 Seal alias system is now active.")
