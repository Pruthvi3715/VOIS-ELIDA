import requests
from bs4 import BeautifulSoup
import re

def debug_rbi():
    url = "https://www.rbi.org.in/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all occurrences of "Repo Rate"
        print("--- All instances of 'Repo Rate' and surrounding text ---")
        targets = soup.find_all(string=re.compile("Repo Rate", re.I))
        for t in targets:
            parent = t.find_parent(['tr', 'td', 'li', 'div', 'p'])
            if parent:
                print(f"Parent ({parent.name}): {parent.get_text(strip=True)}")
        
        # Also look for % sign
        print("\n--- All percentages found in 'Current Rates' or similar divs ---")
        # Usually rates are in a specific table or div
        for tr in soup.find_all('tr'):
            text = tr.get_text(strip=True)
            if '%' in text and any(x in text for x in ["Repo", "Reverse", "MSF", "Bank"]):
                print(f"Row: {text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_rbi()
