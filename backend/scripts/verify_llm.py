import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force reload of config by unimporting if needed, but since this is a new process it should be fine.
from app.core.config import settings
from app.agents.quant import QuantAgent

print(f"Configured LLM Provider: {settings.LLM_PROVIDER}")
print(f"Configured Groq Model: {settings.GROQ_MODEL}")

agent = QuantAgent()
print(f"Agent Provider: {agent.llm_provider}")
print(f"Using Groq: {agent.use_groq}")
print(f"Using Ollama: {agent.use_ollama}")

if agent.use_groq:
    print("✅ SUCCESS: Agent is employing Groq.")
else:
    print("❌ FAILURE: Agent is NOT employing Groq.")
