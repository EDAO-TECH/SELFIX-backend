🛠️ SELFIX-backend/README.md
markdown
Copy
Edit
# SELFIX Backend

The **SELFIX Backend** is the core logic and verification engine behind the SELFIX Trust Framework — a self-healing, logic-verifying system for critical infrastructure. This backend offers healing scripts, antivirus capabilities, license management, trust sealing, and self-recovery features. It powers the operational intelligence behind the frontend interface and CLI.
# Supabase CLI

[![Coverage Status](https://coveralls.io/repos/github/supabase/cli/badge.svg?branch=main)](https://coveralls.io/github/supabase/cli?branch=main) [![Bitbucket Pipelines](https://img.shields.io/bitbucket/pipelines/supabase-cli/setup-cli/master?style=flat-square&label=Bitbucket%20Canary)](https://bitbucket.org/supabase-cli/setup-cli/pipelines) [![Gitlab Pipeline Status](https://img.shields.io/gitlab/pipeline-status/sweatybridge%2Fsetup-cli?label=Gitlab%20Canary)
](https://gitlab.com/sweatybridge/setup-cli/-/pipelines)

[Supabase](https://supabase.io) is an open source Firebase alternative. We're building the features of Firebase using enterprise-grade open source tools.

This repository contains all the functionality for Supabase CLI.

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
=======
- [x] Running Supabase locally
- [x] Managing database migrations
- [x] Creating and deploying Supabase Functions
- [x] Generating types directly from your database schema
- [x] Making authenticated HTTP requests to [Management API](https://supabase.com/docs/reference/api/introduction)

## Getting started

### Install the CLI

Available via [NPM](https://www.npmjs.com) as dev dependency. To install:

```bash
npm i supabase --save-dev
```

To install the beta release channel:

```bash
npm i supabase@beta --save-dev
```

When installing with yarn 4, you need to disable experimental fetch with the following nodejs config.

```
NODE_OPTIONS=--no-experimental-fetch yarn add supabase
```

> **Note**
For Bun versions below v1.0.17, you must add `supabase` as a [trusted dependency](https://bun.sh/guides/install/trusted) before running `bun add -D supabase`.

<details>
  <summary><b>macOS</b></summary>

  Available via [Homebrew](https://brew.sh). To install:

  ```sh
  brew install supabase/tap/supabase
  ```

  To install the beta release channel:
  
  ```sh
  brew install supabase/tap/supabase-beta
  brew link --overwrite supabase-beta
  ```
  
  To upgrade:

  ```sh
  brew upgrade supabase
  ```
</details>

<details>
  <summary><b>Windows</b></summary>

  Available via [Scoop](https://scoop.sh). To install:

  ```powershell
  scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
  scoop install supabase
  ```

  To upgrade:

  ```powershell
  scoop update supabase
  ```
</details>

<details>
  <summary><b>Linux</b></summary>

  Available via [Homebrew](https://brew.sh) and Linux packages.

  #### via Homebrew

  To install:

  ```sh
  brew install supabase/tap/supabase
  ```

  To upgrade:

  ```sh
  brew upgrade supabase
  ```

  #### via Linux packages

  Linux packages are provided in [Releases](https://github.com/supabase/cli/releases). To install, download the `.apk`/`.deb`/`.rpm`/`.pkg.tar.zst` file depending on your package manager and run the respective commands.

  ```sh
  sudo apk add --allow-untrusted <...>.apk
  ```

  ```sh
  sudo dpkg -i <...>.deb
  ```

  ```sh
  sudo rpm -i <...>.rpm
  ```

  ```sh
  sudo pacman -U <...>.pkg.tar.zst
  ```
</details>

<details>
  <summary><b>Other Platforms</b></summary>

  You can also install the CLI via [go modules](https://go.dev/ref/mod#go-install) without the help of package managers.

  ```sh
  go install github.com/supabase/cli@latest
  ```

  Add a symlink to the binary in `$PATH` for easier access:

  ```sh
  ln -s "$(go env GOPATH)/bin/cli" /usr/bin/supabase
  ```

  This works on other non-standard Linux distros.
</details>

<details>
  <summary><b>Community Maintained Packages</b></summary>

  Available via [pkgx](https://pkgx.sh/). Package script [here](https://github.com/pkgxdev/pantry/blob/main/projects/supabase.com/cli/package.yml).
  To install in your working directory:

  ```bash
  pkgx install supabase
  ```

  Available via [Nixpkgs](https://nixos.org/). Package script [here](https://github.com/NixOS/nixpkgs/blob/master/pkgs/development/tools/supabase-cli/default.nix).
</details>

### Run the CLI

```bash
supabase bootstrap
```

Or using npx:

```bash
npx supabase bootstrap
```

The bootstrap command will guide you through the process of setting up a Supabase project using one of the [starter](https://github.com/supabase-community/supabase-samples/blob/main/samples.json) templates.

## Docs

Command & config reference can be found [here](https://supabase.com/docs/reference/cli/about).

## Breaking changes

We follow semantic versioning for changes that directly impact CLI commands, flags, and configurations.

However, due to dependencies on other service images, we cannot guarantee that schema migrations, seed.sql, and generated types will always work for the same CLI major version. If you need such guarantees, we encourage you to pin a specific version of CLI in package.json.

## Developing

To run from source:

```sh
# Go >= 1.22
go run . help
```
