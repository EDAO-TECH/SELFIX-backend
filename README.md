🛠️ SELFIX-backend/README.md
markdown
Copy
Edit
# SELFIX Backend

The **SELFIX Backend** is the core logic and verification engine behind the SELFIX Trust Framework — a self-healing, logic-verifying system for critical infrastructure. This backend offers healing scripts, antivirus capabilities, license management, trust sealing, and self-recovery features. It powers the operational intelligence behind the frontend interface and CLI.

---

## 📦 Project Structure

/opt/SELFIX/
├── selfix/ # Core logic modules and healing engine
├── antivirus/ # Custom antivirus scanner, quarantine & updater
├── forgiveness/ # Trust vault storing sealed, verified logic
├── api/, services/, config/ # Modular services and configurations
├── start_all.sh # Startup launcher for all services
├── selfix_precheck.py # Intelligent system readiness check
├── selfix_smart_start.sh # Smart startup routine
├── selfix_smart_install.sh # Guided installer with dynamic logic checks

yaml
Copy
Edit

---

## ⚙️ Key Features

- **Healing Engine**: Detects, verifies, and restores critical logic files.
- **Antivirus Module**: Custom signature-based malware scanner (`selfix_scanner.py`, `selfix_signatures.json`)
- **License Verification**: SmartLicense-X CLI validation
- **Trust Vault**: Securely seals and restores known-good logic via CLI and audit metadata
- **Forgiveness Targets**: Configurable trust file list (`forgiveness_targets.txt`)
- **Book of Forgiveness**: Stores sealed files, audit logs, and execution hashes
- **Audit and Logging**: Track all sealing/restoring events and file changes

---

## 🔐 Self-Healing Capabilities

- `selfix forgive --seal`: Seal logic to trust vault
- `selfix forgive --verify`: Detect tampering
- `selfix forgive --restore`: Restore trusted files from vault
- `selfix heal`: Automatically fix based on sealed trust

---

## 🧪 Prerequisites

- Python 3.9+
- Linux (Debian/Ubuntu recommended)
- Node.js (if using web control interface)
- Git, curl, systemd

---

## 🛠️ Setup

```bash
# Clone the repository
git clone https://github.com/EDAO-TECH/SELFIX-backend.git

# Enter project folder
cd SELFIX-backend

# Start setup
chmod +x selfix_smart_install.sh
./selfix_smart_install.sh
🧪 Run Antivirus and Healing Logic
bash
Copy
Edit
# Run precheck
python3 selfix_smart_precheck.py

# Launch services
./start_all.sh
📁 Trust Logic Example (CRITICAL_FILES)
python
Copy
Edit
CRITICAL_FILES = [
  "/opt/SELFIX/selfix/engine/healing_manager.py",
  "/opt/SELFIX/selfix/scripts/selfix_heal.py",
  "/opt/SELFIX/selfix/scripts/selfix_precheck.py",
  "/opt/SELFIX/selfix/cli/selfix.py",
  "/opt/SELFIX/selfix/configs/ai_policy.json"
]
🧩 Sealing Trusted Logic
bash
Copy
Edit
# Tier 1
selfix forgive --seal all

# Tier 2 (forgiveness_targets.txt)
selfix forgive --seal /opt/SELFIX/customers/bankcorp/modules/bank_healer.py
📜 License
This project is licensed under the SELFIX Ethical License. Contact EDAO-TECH for commercial deployment and licensing terms.

🤝 Contact & Support
EDAO-TECH
Email: support@edao.tech
GitHub: https://github.com/EDAO-TECH

yaml
Copy
Edit

---

## 🌐 `SELFIX-frontend/README.md`

```markdown
# SELFIX Frontend

The **SELFIX Frontend** provides a modern web-based interface to interact with the SELFIX backend healing engine, antivirus status, trust vault, and license status. Built with Vite + React and styled using TailwindCSS, this interface enables customers to monitor system health, manage trusted logic, and visualize healing status.

---

## 📦 Project Structure
