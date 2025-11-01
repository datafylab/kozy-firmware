# config.py
import json
import os

CONFIG_FILE = "rsc1_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"resolution": "1280x720", "fps": 30}

def save_config(resolution: str, fps: int):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"resolution": resolution, "fps": fps}, f, indent=4)
        return True
    except Exception as e:
        return False
