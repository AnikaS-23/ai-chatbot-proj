import requests
import sys
import json

BASE_URL = "http://127.0.0.1:8000"

try:
    print(f"Testing connection to {BASE_URL}/...")
    try:
        r = requests.get(f"{BASE_URL}/", timeout=2)
        print(f"Root status: {r.status_code}")
        print(f"Root response: {r.text}")
    except Exception as e:
        print(f"Root connection failed: {e}")

    print("\nTesting chat endpoint...")
    payload = {
        "message": "Hello",
        "history": []
    }
    try:
        r = requests.post(f"{BASE_URL}/chat", json=payload, timeout=10)
        print(f"Chat status: {r.status_code}")
        print(f"Chat response: {json.dumps(r.json(), indent=2)}")
    except Exception as e:
         print(f"Chat request failed: {e}")
         if 'r' in locals() and r:
             print(f"Raw response: {r.text}")

except Exception as e:
    print(f"\nCritical failure: {e}")
