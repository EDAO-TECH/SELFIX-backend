import os, tarfile

ARCHIVE_DIR = "/opt/SELFIX/archive/components/"

def rollback(component_id):
    tar_path = os.path.join(ARCHIVE_DIR, f"{component_id}.tar.gz")
    if not os.path.exists(tar_path):
        return f"❌ No rollback found for {component_id}"
    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall("/")
        return f"✅ Rolled back: {component_id}"
    except Exception as e:
        return f"❌ Rollback failed: {e}"
