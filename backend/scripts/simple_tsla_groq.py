"""
Simple TSLA Stock Analysis - Direct Groq API Call
Uses openai/gpt-oss-120b model
"""
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# Static TSLA data
TSLA_DATA = {
    "symbol": "TSLA",
    "name": "Tesla, Inc.",
    "current_price": 421.06,
    "market_cap": 1350000000000,
    "pe_ratio": 180.5,
    "forward_pe": 95.2,
    "eps": 2.33,
    "52w_high": 488.54,
    "52w_low": 138.80,
    "beta": 2.31,
    "sector": "Consumer Cyclical",
    "industry": "Auto Manufacturers",
    "summary": "Tesla is the world's leading electric vehicle manufacturer and clean energy company."
}

def analyze_with_groq(stock_data: dict) -> str:
    """Send stock data to Groq for analysis."""
    
    prompt = f"""Analyze Tesla (TSLA) stock based on this data:

Current Price: ${stock_data['current_price']}
Market Cap: $1.35 Trillion
P/E Ratio: {stock_data['pe_ratio']}
52-Week Range: ${stock_data['52w_low']} - ${stock_data['52w_high']}
Beta: {stock_data['beta']}

Provide a brief investment analysis with:
1. Score (0-100)
2. Buy/Hold/Sell recommendation
3. 2 strengths
4. 2 risks
5. One-paragraph summary"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful financial analyst assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }
    
    print(f"🧠 Calling Groq ({MODEL})...")
    
    response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        error = response.json()
        print(f"❌ Error: {error}")
        return None

def main():
    print("\n" + "="*60)
    print("🚀 TSLA (Tesla) Stock Analysis - Groq API")
    print("="*60)
    
    stock_data = TSLA_DATA
    
    print("\n📊 KEY METRICS:")
    print(f"   • Price: ${stock_data['current_price']}")
    print(f"   • Market Cap: $1.35T")
    print(f"   • P/E: {stock_data['pe_ratio']}")
    print(f"   • 52W: ${stock_data['52w_low']} - ${stock_data['52w_high']}")
    print(f"   • Beta: {stock_data['beta']}\n")
    
    analysis = analyze_with_groq(stock_data)
    
    if analysis and len(analysis) > 50:
        print("="*60)
        print("🤖 AI ANALYSIS")
        print("="*60)
        print(analysis)
        print("\n" + "="*60)
        print("✅ Complete!")
        print("="*60 + "\n")
    else:
        print(f"Response: {analysis}")
        print("❌ Model didn't provide useful analysis")

if __name__ == "__main__":
    main()
