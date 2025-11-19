# config.py
import json
import os

CONFIG_FILE = "rsc1_config.json"

def load_config():
    """Load configuration from file, with default values if file doesn't exist."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as config_file:
                return json.load(config_file)
        except Exception:
            pass
    return {"resolution": "1280x720", "fps": 30}

def save_config(resolution: str, fps: int):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as config_file:
            json.dump({"resolution": resolution, "fps": fps}, config_file, indent=4)
        return True
    except Exception as e:
        return False
