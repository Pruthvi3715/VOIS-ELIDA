import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in env.")
    exit(1)

genai.configure(api_key=api_key)

models_to_test = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "models/gemini-2.5-flash-native-audio-preview-12-2025",
    "gemini-pro"
]

print(f"Testing Gemini API with Key: {api_key[:5]}...{api_key[-4:]}")

for model_name in models_to_test:
    print(f"\n--- Testing Model: {model_name} ---")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, can you hear me?")
        print(f"✅ SUCCESS! Response: {response.text}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
