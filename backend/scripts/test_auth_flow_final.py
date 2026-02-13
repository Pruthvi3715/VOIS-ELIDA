import requests
import sys
import uuid

BASE_URL = "http://localhost:8000/api"

def test_auth_flow():
    # 1. Register a new user
    random_id = str(uuid.uuid4())[:8]
    username = f"testuser_{random_id}"
    email = f"test_{random_id}@example.com"
    password = "password123"

    print(f"--- Testing Registration for {username} ---")
    reg_payload = {
        "username": username,
        "email": email,
        "password": password
    }
    
    try:
        reg_resp = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
        if reg_resp.status_code == 200:
            print("✅ Registration Successful")
            print(f"Response: {reg_resp.json()}")
        else:
            print(f"❌ Registration Failed: {reg_resp.status_code} - {reg_resp.text}")
            return
    except Exception as e:
        print(f"❌ Connection Error during Register: {e}")
        return

    # 2. Login with the new user
    print(f"\n--- Testing Login for {username} ---")
    login_payload = {
        "username": username,
        "password": password
    }
    
    token = None
    try:
        login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        if login_resp.status_code == 200:
            print("✅ Login Successful")
            data = login_resp.json()
            token = data.get("access_token")
            print(f"Token received: {token[:20]}...")
        else:
            print(f"❌ Login Failed: {login_resp.status_code} - {login_resp.text}")
            return
    except Exception as e:
        print(f"❌ Connection Error during Login: {e}")
        return

    # 3. Test Protected Endpoint (e.g., /analyze/ITC.NS with token)
    # Note: /analyze/ uses get_current_user_optional, so it should see the user ID now.
    print(f"\n--- Testing Protected Endpoint with Token ---")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # We use a known ticker like ITC.NS
        # We look for debug logs in the backend output (via previous tasks) but here we check status code
        analyze_resp = requests.get(f"http://localhost:8000/analyze/ITC.NS", headers=headers)
        if analyze_resp.status_code == 200:
             print("✅ Protected Access Successful")
             # Verify it processed as a user? Difficult from client side without specific response field, 
             # but success means auth didn't crash it.
        else:
             print(f"❌ Protected Access Failed: {analyze_resp.status_code} - {analyze_resp.text}")

    except Exception as e:
        print(f"❌ Connection Error during Protected Access: {e}")

if __name__ == "__main__":
    test_auth_flow()
