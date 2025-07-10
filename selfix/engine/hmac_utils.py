import os
import hmac
import hashlib
import base64

def load_secret(path):
    """Load or create a 256-bit (32-byte) secret key."""
    if not os.path.exists(path):
        key = os.urandom(32)
        with open(path, "wb") as f:
            f.write(key)
    with open(path, "rb") as f:
        return f.read()

def sign_manifest(manifest_path, sig_path, key_path):
    """Sign the manifest file and store base64-encoded HMAC."""
    key = load_secret(key_path)
    with open(manifest_path, "rb") as f:
        content = f.read()
    sig = hmac.new(key, content, hashlib.sha256).digest()
    with open(sig_path, "wb") as f:
        f.write(base64.b64encode(sig))

def verify_manifest(manifest_path, sig_path, key_path):
    """Verify HMAC signature of manifest.json."""
    key = load_secret(key_path)
    with open(manifest_path, "rb") as f:
        content = f.read()

    if not os.path.exists(sig_path):
        raise ValueError("❌ Signature file missing: cannot validate manifest.")

    with open(sig_path, "rb") as f:
        stored_sig = base64.b64decode(f.read())

    expected_sig = hmac.new(key, content, hashlib.sha256).digest()

    if not hmac.compare_digest(stored_sig, expected_sig):
        raise ValueError("🚨 Manifest verification FAILED — possible tampering detected.")

    # Optional: return True for logging/debug
    return True
