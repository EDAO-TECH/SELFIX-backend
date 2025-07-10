import os

# Dynamically resolve project root (portable USB/VPS)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

PATHS = {
    "ROOT": ROOT,
    "MANIFEST": os.path.join(ROOT, "forgiveness/meta/manifest.json"),
    "SIGNATURE": os.path.join(ROOT, "forgiveness/meta/manifest.sig"),
    "SECRET_KEY": os.path.join(ROOT, "selfix/engine/secret.key")
}
