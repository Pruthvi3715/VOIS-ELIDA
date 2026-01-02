import requests
from bs4 import BeautifulSoup
import re

class RBIService:
    """
    Service to fetch real-time data from Reserve Bank of India (RBI).
    """
    URL = "https://www.rbi.org.in/"

    def get_real_time_rates(self):
        """
        Scrape RBI website for latest Policy Repo Rate.
        Returns: {'repo_rate': float} or {'error': str}
        """
        try:
            # RBI blocks generic user agents sometimes, use browser-like
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.URL, timeout=10, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Strategy 1: Find "Policy Repo Rate" text and look for number in same row
            # The RBI site usually has a "Current Rates" section
            
            target_text = "Policy Repo Rate"
            # Find element containing text
            elements = soup.find_all(string=re.compile(target_text))
            
            for el in elements:
                # Traverse up to a container (like TR or LI)
                parent = el.find_parent(['tr', 'li', 'div'])
                if parent:
                    text = parent.get_text()
                    # Look for pattern: 6.50% or 6.50
                    # Regex for percentage value
                    match = re.search(r':?\s*(\d+\.\d+)\s*%', text)
                    if match:
                        return {"repo_rate": float(match.group(1))}
            
            return {"error": "Could not parse Repo Rate. Site structure may have changed."}
            
        except Exception as e:
            return {"error": f"Scraping failed: {e}"}

# Singleton
rbi_service = RBIService()
