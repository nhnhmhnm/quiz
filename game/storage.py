import json
import os
from config import STATE_FILE, ENCODING

def _default_state():
    return {"quizzes": [], "history": []}

def load_state():
    if not os.path.exists(STATE_FILE):
        return _default_state()
    try:
        with open(STATE_FILE, "r", encoding=ENCODING) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("파일이 손상되었습니다. 새로 시작합니다.")
        return _default_state()

def save_state(state):
    with open(STATE_FILE, "w", encoding=ENCODING) as f:
        json.dump(state, f, ensure_ascii=False, indent=2)