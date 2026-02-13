import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.base import BaseAgent
from app.core.config import settings

# Force OpenRouter provider for test
settings.LLM_PROVIDER = "openrouter"

class AnalystAgent(BaseAgent):
    def run(self, ticker):
        prompt = f"Analyze the stock {ticker}. Give me a brief summary of its business and current market standing."
        return self.call_llm(prompt)

def test_stock_analysis(ticker="AAPL"):
    print(f"Testing Stock Analysis for {ticker} using OpenRouter...")
    print(f"Provider: {settings.LLM_PROVIDER}")
    print(f"Model: {settings.OPENROUTER_MODEL}")
    
    agent = AnalystAgent("Analyst")
    
    if not agent.use_openrouter:
        print("ERROR: Agent is not configured to use OpenRouter!")
        return
        
    print(f"Agent configured: {agent.use_openrouter}")
    
    try:
        response = agent.run(ticker)
        print(f"\nAnalysis Result:\n{response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with Apple Inc.
    test_stock_analysis("AAPL")
