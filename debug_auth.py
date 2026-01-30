import requests
import json

URL = "http://localhost:8000"

def test_login(username, password):
    print(f"Testing login for {username}...")
    try:
        resp = requests.post(f"{URL}/login", json={"username": username, "password": password})
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

# Try to login with known user "anika" (we don't know the password but we can see if it returns 401 vs Connection Error)
# or register a test user
test_login("test_user_debug", "test_pass") 

def register_test():
    print("Registering test user...")
    try:
        resp = requests.post(f"{URL}/register", json={"username": "test_user_debug", "password": "test_pass"})
        print(f"Register Status: {resp.status_code}")
        print(f"Register Response: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

register_test()
test_login("test_user_debug", "test_pass")
