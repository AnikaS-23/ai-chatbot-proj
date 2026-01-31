import requests
import uuid

BASE_URL = "http://localhost:8000"
USERNAME = f"testuser_{uuid.uuid4().hex[:6]}"
PASSWORD = "testpassword123"

def test_auth():
    print(f"Testing with user: {USERNAME}")
    
    # 1. Register
    print("Registering...")
    resp = requests.post(f"{BASE_URL}/register", json={"username": USERNAME, "password": PASSWORD})
    print(f"Register Status: {resp.status_code}")
    print(f"Register Response: {resp.text}")
    
    if resp.status_code != 200:
        return

    # 2. Login
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/login", json={"username": USERNAME, "password": PASSWORD})
    print(f"Login Status: {resp.status_code}")
    print(f"Login Response: {resp.text}")

if __name__ == "__main__":
    test_auth()
