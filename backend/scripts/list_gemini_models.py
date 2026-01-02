import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.environ.get("GEMINI_API_KEY")

print(f"Listing models for Key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")
except Exception as e:
    print(f"Failed to list models! Error: {e}")
