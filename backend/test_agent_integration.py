import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.base import BaseAgent
from app.core.config import settings

# Force OpenRouter provider for test
settings.LLM_PROVIDER = "openrouter"

class TestAgent(BaseAgent):
    def run(self, context):
        pass

def test_openrouter_integration():
    print(f"Testing OpenRouter Integration...")
    print(f"Provider: {settings.LLM_PROVIDER}")
    print(f"Model: {settings.OPENROUTER_MODEL}")
    
    agent = TestAgent("TestAgent")
    
    if not agent.use_openrouter:
        print("ERROR: Agent is not configured to use OpenRouter!")
        return
    
    print(f"Agent configured for OpenRouter: {agent.use_openrouter}")
    
    response = agent.call_llm("Hello, are you working via OpenRouter?")
    print(f"\nResponse: {response}")
    
    if "OpenRouter" in str(response) or len(response) > 5:
        print("\nSUCCESS: Received response from OpenRouter.")
    else:
        print("\nFAILURE: No valid response received.")

if __name__ == "__main__":
    test_openrouter_integration()
