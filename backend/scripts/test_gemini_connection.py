
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, "..", ".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

print(f"Testing Gemini API with model: {model_name}")
print(f"API Key present: {'Yes' if api_key else 'No'}")

if not api_key:
    print("Error: GEMINI_API_KEY not found in environment.")
    exit(1)

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello, simply say 'Connection Successful' if you can hear me.")
    print(f"\nResponse from Gemini: {response.text}")
    print("\n✅ Verification Successful!")
    with open("test_gemini_result.txt", "w") as f:
        f.write("SUCCESS: " + response.text)
except Exception as e:
    print(f"\n❌ Verification Failed: {e}")
    with open("test_gemini_result.txt", "w") as f:
        f.write(f"FAILURE: {e}")
    
    print("\nAttempting to list available models...")
    try:
        for m in genai.list_models():
            print(f"- {m.name}")
    except Exception as list_e:
        print(f"Could not list models: {list_e}")
