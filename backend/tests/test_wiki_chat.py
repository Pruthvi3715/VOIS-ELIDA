import requests
import json

def test_chat(query):
    url = "http://localhost:8000/chat/general"
    payload = {"query": query}
    try:
        response = requests.post(url, json=payload)
        print(f"Query: {query}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json().get('response', 'No response')}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_chat("What is systemic risk?")
    test_chat("meaning of ROI")
    test_chat("asdfghjkl") # Should fail gracefully
