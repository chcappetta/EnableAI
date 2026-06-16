import os
import json
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)

    except FileNotFoundError:
        return {}
    
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def login():
    users = load_users()

    username = input("Username: ")

    if username not in users:
        print("User not found.")
        return None

    password = input("Password: ")

    if not verify_password(
        password,
        users[username]
    ):
        print("Incorrect password.")
        return None

    print("Login successful.")

    return username 

def register():
    users = load_users()
    username = input("Username: ")
    if username in users:
        print("Username taken.")
        return None
    password = input("Password: ")
    confirm = input("Confirm Password: ")
    if password != confirm:
        print("Passwords do not match.")
        return None
    users[username] = hash_password(password)
    save_users(users)
    os.makedirs(
        f"data/users/{username}",
        exist_ok=True
    )
    print("Registration successful.")
    return username



