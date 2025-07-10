from selfix.engine.book_of_forgiveness import _load_manifest, is_trusted_entry

manifest = _load_manifest()

print("\n📜 Book of Forgiveness Debugger\n")

for file_path, versions in manifest.items():
    print(f"🔍 {file_path}")
    for v in versions:
        forgiven = v.get("forgiven_by", "<none>")
        reason = v.get("reason", "<none>")
        print(f"  🔖 Forgiven by: {forgiven}")
        print(f"  ✏️ Reason: {reason}")
        if is_trusted_entry(v):
            print("  ✅ Trusted entry\n")
        else:
            print("  ❌ NOT trusted\n")
