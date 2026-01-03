
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/tags"

print(f"Testing Ollama Connection at: {OLLAMA_URL}")

try:
    response = requests.get(OLLAMA_URL, timeout=5)
    if response.status_code == 200:
        print("✅ Connection Successful!")
        data = response.json()
        models = [model['name'] for model in data.get('models', [])]
        print("\nAvailable Models:")
        for m in models:
            print(f"- {m}")
        
        # Check if qwen2.5:7b is present (recommended model)
        if "qwen2.5:7b" in models:
             print("\n✅ Recommended model 'qwen2.5:7b' is available.")
        else:
             print("\n⚠️ Recommended model 'qwen2.5:7b' NOT found.")
    else:
        print(f"❌ Connection Failed with Status Code: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ Connection Failed: Could not connect to localhost:11434. Is Ollama running?")
except Exception as e:
    print(f"❌ An error occurred: {e}")
