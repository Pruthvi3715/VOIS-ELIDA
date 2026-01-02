import requests
from bs4 import BeautifulSoup
import urllib.parse

def test_google_scrape(query):
    print(f"Searching for: {query}")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=5)
    print(f"Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Try finding featured snippet
    answer = ""
    snippet_classes = ["hgKElc", "V3FYCf", "BNeawe", "LGOjhe", "Z0LcW"]
    for cls in snippet_classes:
        element = soup.find(class_=cls)
        if element:
            answer = element.get_text()
            print(f"Found snippet via class {cls}")
            break
            
    if not answer:
        print("No snippet found, trying fallback...")
        # Fallback to meta description or first result
        results = soup.select("div.g")
        if results:
            answer = results[0].get_text()[:200]
            print("Found fallback result")

    print(f"\nFinal Answer: {answer}")

if __name__ == "__main__":
    test_google_scrape("What is specific risk?")
