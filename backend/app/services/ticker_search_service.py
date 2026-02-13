# Smart Ticker Search Service
# Converts company names to ticker symbols using DuckDuckGo search

import requests
from typing import Optional, Tuple
import re

# Common Indian stock mappings (fast lookup)
INDIAN_STOCK_MAPPING = {
    # Major Companies
    "reliance": "RELIANCE.NS",
    "reliance industries": "RELIANCE.NS",
    "tata consultancy": "TCS.NS",
    "tcs": "TCS.NS",
    "tata motors": "TATAMOTORS.NS",
    "infosys": "INFY.NS",
    "hdfc bank": "HDFCBANK.NS",
    "hdfc": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS",
    "icici": "ICICIBANK.NS",
    "sbi": "SBIN.NS",
    "state bank": "SBIN.NS",
    "state bank of india": "SBIN.NS",
    "wipro": "WIPRO.NS",
    "hcl tech": "HCLTECH.NS",
    "hcl technologies": "HCLTECH.NS",
    "bharti airtel": "BHARTIARTL.NS",
    "airtel": "BHARTIARTL.NS",
    "itc": "ITC.NS",
    "hindustan unilever": "HINDUNILVR.NS",
    "hul": "HINDUNILVR.NS",
    "asian paints": "ASIANPAINT.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "kotak mahindra": "KOTAKBANK.NS",
    "kotak bank": "KOTAKBANK.NS",
    "maruti suzuki": "MARUTI.NS",
    "maruti": "MARUTI.NS",
    "larsen & toubro": "LT.NS",
    "l&t": "LT.NS",
    "axis bank": "AXISBANK.NS",
    "sun pharma": "SUNPHARMA.NS",
    "titan": "TITAN.NS",
    "ultra tech cement": "ULTRACEMCO.NS",
    "ultratech": "ULTRACEMCO.NS",
    "power grid": "POWERGRID.NS",
    "ntpc": "NTPC.NS",
    "ongc": "ONGC.NS",
    "coal india": "COALINDIA.NS",
    "tech mahindra": "TECHM.NS",
    "nestle india": "NESTLEIND.NS",
    "nestle": "NESTLEIND.NS",
    "tata steel": "TATASTEEL.NS",
    "adani enterprises": "ADANIENT.NS",
    "adani ports": "ADANIPORTS.NS",
    "bajaj auto": "BAJAJ-AUTO.NS",
    "dr reddy": "DRREDDY.NS",
    "dr reddys": "DRREDDY.NS",
    "britannia": "BRITANNIA.NS",
    "cipla": "CIPLA.NS",
    "grasim": "GRASIM.NS",
    "divis labs": "DIVISLAB.NS",
    "divis": "DIVISLAB.NS",
    "indusind bank": "INDUSINDBK.NS",
    "hero motocorp": "HEROMOTOCO.NS",
    "hero": "HEROMOTOCO.NS",
    "hindalco": "HINDALCO.NS",
    "jio financial": "JIOFIN.NS",
    "jio": "JIOFIN.NS",
    "jsw steel": "JSWSTEEL.NS",
    "m&m": "M&M.NS",
    "mahindra": "M&M.NS",
    "mahindra and mahindra": "M&M.NS",
    "eicher motors": "EICHERMOT.NS",
    "shriram finance": "SHRIRAMFIN.NS",
    "tata consumer": "TATACONSUM.NS",
    "zomato": "ZOMATO.NS",
    "paytm": "PAYTM.NS",
    "dmart": "DMART.NS",
    "avenue supermarts": "DMART.NS",
    "vedanta": "VEDL.NS",
    
    # US Stocks
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "netflix": "NFLX",
    "amd": "AMD",
    "intel": "INTC",
    "ibm": "IBM",
    "coca cola": "KO",
    "coke": "KO",
    "pepsi": "PEP",
    "pepsico": "PEP",
    "disney": "DIS",
    "walmart": "WMT",
    "nike": "NKE",
    "visa": "V",
    "mastercard": "MA",
    "jpmorgan": "JPM",
    "goldman sachs": "GS",
    "berkshire": "BRK-B",
    "berkshire hathaway": "BRK-B",
}


def search_ticker_local(company_name: str) -> Optional[str]:
    """
    Quick local lookup for common company names.
    Returns ticker symbol if found, None otherwise.
    """
    name_lower = company_name.lower().strip()
    
    # Direct match
    if name_lower in INDIAN_STOCK_MAPPING:
        return INDIAN_STOCK_MAPPING[name_lower]
    
    # Partial match
    for key, ticker in INDIAN_STOCK_MAPPING.items():
        if key in name_lower or name_lower in key:
            return ticker
    
    return None


def search_ticker_duckduckgo(company_name: str) -> Optional[str]:
    """
    Search for ticker symbol using DuckDuckGo.
    Returns ticker symbol if found, None otherwise.
    """
    try:
        # Use DuckDuckGo instant answer API
        query = f"{company_name} stock ticker symbol NSE BSE"
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Check Abstract for ticker pattern
            abstract = data.get("Abstract", "") + data.get("AbstractText", "")
            
            # Look for NSE/BSE tickers
            nse_pattern = r'\b([A-Z]{2,15})\.NS\b'
            bse_pattern = r'\b([A-Z]{2,15})\.BO\b'
            us_pattern = r'\b(NYSE|NASDAQ):\s*([A-Z]{1,5})\b'
            
            # Try NSE first
            nse_match = re.search(nse_pattern, abstract)
            if nse_match:
                return f"{nse_match.group(1)}.NS"
            
            # Try BSE
            bse_match = re.search(bse_pattern, abstract)
            if bse_match:
                return f"{bse_match.group(1)}.BO"
            
            # Try US stocks
            us_match = re.search(us_pattern, abstract)
            if us_match:
                return us_match.group(2)
        
        # Fallback: Try a simple web search scrape
        search_url = f"https://html.duckduckgo.com/html/?q={company_name}+stock+ticker+NSE"
        response = requests.get(search_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            # Look for ticker patterns in results
            content = response.text.upper()
            
            # Check for common patterns
            nse_matches = re.findall(r'\b([A-Z]{2,15})\.NS\b', content)
            if nse_matches:
                return f"{nse_matches[0]}.NS"
            
            bse_matches = re.findall(r'\b([A-Z]{2,15})\.BO\b', content)
            if bse_matches:
                return f"{bse_matches[0]}.BO"
    
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
    
    return None


def resolve_company_to_ticker(input_text: str) -> Tuple[str, str]:
    """
    Main function: Resolve company name or ticker to a valid ticker symbol.
    
    Returns:
        Tuple of (ticker, source) where source is 'exact', 'local', 'search', or 'passthrough'
    """
    text = input_text.strip()
    
    # 1. Check if it's already a valid ticker format
    if re.match(r'^[A-Z]{1,15}(\.(NS|BO))?$', text.upper()):
        # Already looks like a ticker
        return text.upper(), "exact"
    
    # 2. Try local mapping first (fastest)
    local_result = search_ticker_local(text)
    if local_result:
        return local_result, "local"
    
    # 3. Try DuckDuckGo search (slower but comprehensive)
    search_result = search_ticker_duckduckgo(text)
    if search_result:
        return search_result, "search"
    
    # 4. Fallback: Return as-is (uppercase) and let Yahoo Finance try
    return text.upper().replace(" ", ""), "passthrough"


def get_ticker_suggestions(partial_input: str, limit: int = 5) -> list:
    """
    Get ticker suggestions for autocomplete based on partial input.
    """
    partial_lower = partial_input.lower().strip()
    suggestions = []
    
    for name, ticker in INDIAN_STOCK_MAPPING.items():
        if partial_lower in name or name.startswith(partial_lower):
            suggestions.append({
                "name": name.title(),
                "ticker": ticker
            })
            if len(suggestions) >= limit:
                break
    
    return suggestions
