import sys
import requests

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing /auth/register...")
    resp = requests.post(
        f"{base_url}/auth/register",
        json={"email": "test@test.com", "password": "password123", "full_name": "Test User"}
    )
    print(f"Register status: {resp.status_code}")
    print(f"Register body: {resp.text}")
    
    print("Testing /auth/login...")
    resp = requests.post(
        f"{base_url}/auth/login",
        json={"email": "test@test.com", "password": "password123"}
    )
    print(f"Login status: {resp.status_code}")
    print(f"Login body: {resp.text}")

if __name__ == "__main__":
    test_api()
