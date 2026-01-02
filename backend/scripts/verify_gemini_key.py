import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.environ.get("GEMINI_API_KEY")

print(f"Testing Gemini Key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Hello, are you working?")
    print(f"Success! Gemini says: {response.text}")
except Exception as e:
    print(f"Failed! Error: {e}")
