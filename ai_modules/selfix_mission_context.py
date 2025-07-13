import os
import json
import logging
from datetime import datetime

# Absolute paths to log and data folders
BASE_DIR = "/opt/SELFIX"
CONTEXT_PATH = os.path.join(BASE_DIR, "data", "mission_context.json")
LOG_PATH = os.path.join(BASE_DIR, "logs", "mission_context.log")

# Setup logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class MissionContext:
    def __init__(self):
        self.context_path = CONTEXT_PATH
        self.default_context = {
            "mission": "frontend_generation",
            "status": "ready",
            "last_prompt": "",
            "last_generated": None,
            "meta": {
                "version": "1.0.0",
                "source": "selfix_ai"
            }
        }
        self.context = {}
        self._load()

    def _load(self):
        """Load mission context from JSON or reinitialize."""
        if not os.path.exists(self.context_path):
            logging.warning("Context file missing. Initializing with defaults.")
            self._save(self.default_context)
            self.context = self.default_context
            return

        if os.path.getsize(self.context_path) == 0:
            logging.warning("Context file is empty. Reinitializing.")
            self._save(self.default_context)
            self.context = self.default_context
            return

        try:
            with open(self.context_path, "r") as f:
                self.context = json.load(f)

            if not self._validate(self.context):
                logging.error("Invalid schema. Reverting to defaults.")
                self._save(self.default_context)
                self.context = self.default_context

        except json.JSONDecodeError:
            logging.exception("JSON decode error. Reinitializing file.")
            self._save(self.default_context)
            self.context = self.default_context

    def _save(self, context_data=None):
        """Write context to disk."""
        context_data = context_data or self.context
        try:
            os.makedirs(os.path.dirname(self.context_path), exist_ok=True)
            with open(self.context_path, "w") as f:
                json.dump(context_data, f, indent=4)
            logging.info("Context saved successfully.")
        except Exception as e:
            logging.exception("Failed to save context.")

    def _validate(self, ctx):
        """Basic schema validation."""
        required_keys = ["mission", "status", "meta"]
        return all(k in ctx for k in required_keys)

    def update(self, key, value):
        """Update a top-level key in context and persist."""
        self.context[key] = value
        self._save()

    def mark_generated(self, prompt: str):
        """Set generation metadata after a prompt run."""
        self.context["last_prompt"] = prompt
        self.context["last_generated"] = datetime.utcnow().isoformat()
        self.context["status"] = "completed"
        self._save()

    def reset(self):
        """Reset context to default values."""
        self.context = self.default_context.copy()
        self._save()
        logging.info("Context reset to defaults.")

    def get(self, key, default=None):
        """Safe getter for context."""
        return self.context.get(key, default)

    def as_dict(self):
        """Return full context."""
        return self.context
