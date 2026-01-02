
import requests
import json

def test_general_search(query):
    url = "http://localhost:8000/chat/general"
    try:
        response = requests.post(url, json={"query": query})
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_general_search("what is rsi indicator")
