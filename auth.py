import json
import os
import bcrypt
import uuid

USERS_FILE = "users.json"

def load_data():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def register_user(username, password):
    data = load_data()
    if username in data:
        return False, "Username already exists"
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    data[username] = {
        "password": hashed,
        "chats": {}
    }
    save_data(data)
    return True, "User registered successfully"

def authenticate_user(username, password):
    data = load_data()
    if username not in data:
        return False
    
    stored_hash = data[username]["password"]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True
    return False

def save_chat(username, chat_id, title, messages):
    data = load_data()
    if username in data:
        data[username]["chats"][chat_id] = {
            "title": title,
            "messages": messages
        }
        save_data(data)

def load_user_chats(username):
    data = load_data()
    return data.get(username, {}).get("chats", {})

def clear_user_history(username):
    data = load_data()
    if username in data:
        data[username]["chats"] = {}
        save_data(data)
        return True
    return False
