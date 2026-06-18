import json
import os

def load_profile(user_name):
    path = f"data/users/{user_name}/profile.json"

    try:
        with open(path, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        return {}

def save_profile(user_name, profile):

    path = f"data/users/{user_name}/profile.json"

    os.makedirs(
        f"data/users/{user_name}",
        exist_ok=True
    )

    with open(path, "w") as f:
        json.dump(profile, f, indent=2)

def remember_tool(ai_name, user_name, args):

    parts = args.split(maxsplit=1)

    if len(parts) < 2:
        return "Usage: /remember <key> <value>"

    key = parts[0]
    value = parts[1]

    profile = load_profile(user_name)

    profile[key] = value

    save_profile(user_name, profile)

    return f"Remembered {key}: {value}"

def profile_tool(ai_name, user_name, args):

    profile = load_profile(user_name)

    if not profile:
        return "No profile information stored."

    output = ""

    for key, value in profile.items():
        output += f"{key}: {value}\n"

    return output
