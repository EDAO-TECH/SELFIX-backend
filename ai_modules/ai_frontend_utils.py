import subprocess
import os
from datetime import datetime

MODEL_NAME = "mistral"

def generate_frontend_with_ollama(prompt: str) -> str:
    try:
        proc = subprocess.Popen(
            ["ollama", "run", MODEL_NAME],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = proc.communicate(input=prompt)

        if proc.returncode != 0:
            raise RuntimeError(f"Ollama failed: {stderr.strip()}")

        return stdout

    except FileNotFoundError:
        raise EnvironmentError("Ollama CLI not found. Is it installed and in your PATH?")
    except Exception as e:
        raise RuntimeError(f"Error generating frontend: {str(e)}")

def save_generated_html(html: str, filename: str = None) -> str:
    target_dir = os.path.join("frontend", "generated")
    os.makedirs(target_dir, exist_ok=True)

    if not filename:
        filename = f"generated_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html"

    file_path = os.path.join(target_dir, filename)

    with open(file_path, "w") as f:
        f.write(html)

    return file_path
