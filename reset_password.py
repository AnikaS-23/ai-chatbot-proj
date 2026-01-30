import bcrypt
import json

USERS_FILE = "users.json"

def reset_password(username, new_password):
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
        
        if username in data:
            print(f"Resetting password for {username}...")
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            data[username]["password"] = hashed
            
            with open(USERS_FILE, "w") as f:
                json.dump(data, f, indent=4)
            print("Password reset successful.")
        else:
            print(f"User {username} not found.")

    except Exception as e:
        print(f"Error: {e}")

reset_password("anika", "password123")
