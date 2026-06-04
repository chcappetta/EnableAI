import json
import os

def load_history(user_name, ai_name):
    path = f"data/users/{user_name}/history.json"
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [
            {
                "role": "system",
                "content": f"You are a helpful AI assistant named {ai_name}."
            }
        ]
    
def save_history(user_name, messages):
    os.makedirs(f"data/users/{user_name}", exist_ok=True)
    with open(f"data/users/{user_name}/history.json", "w") as f:
        json.dump(messages, f, indent=2)
