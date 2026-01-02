import requests
import json

BASE_URL = "http://localhost:8000"

def test_profile():
    user_id = "default_user"
    print(f"🚀 Testing Profile API for {user_id}...")
    
    # 1. Update Profile with Custom Rules
    payload = {
        "user_id": user_id,
        "risk_tolerance": "aggressive",
        "custom_rules": ["Avoid airline stocks", "Focus on AI"]
    }
    
    print("\n1️⃣  Updating Profile...")
    res = requests.post(f"{BASE_URL}/api/v1/profile", json=payload)
    print(f"   Status: {res.status_code}")
    print(f"   Response: {res.text}")
    
    # 2. Get Profile
    print("\n2️⃣  Retrieving Profile...")
    res = requests.get(f"{BASE_URL}/api/v1/profile/{user_id}")
    if res.status_code == 200:
        data = res.json()
        profile = data.get("profile", {})
        print(f"   User ID: {profile.get('user_id')}")
        print(f"   Custom Rules: {profile.get('custom_rules')}")
        
        if "Avoid airline stocks" in profile.get("custom_rules", []):
            print("\n✅ SUCCESS: Rule persisted!")
        else:
            print("\n❌ ID MATCH FAILED or RULES MISSING")
            print(json.dumps(profile, indent=2))
    else:
        print(f"   ❌ Error: {res.status_code}")

if __name__ == "__main__":
    test_profile()
