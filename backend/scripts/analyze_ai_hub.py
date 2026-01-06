"""
Analyze AI Engineering Hub using Groq OSS-120B
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

CONTENT = """
AI Engineering Hub - 93+ Production-Ready AI Projects

BEGINNER (22): OCR (LaTeX, Llama, Gemma, Qwen), Chat UIs (DeepSeek, Llama, Gemma), 
Basic RAG (LlamaIndex, Qdrant), Video RAG, Image Gen (Janus-Pro)

INTERMEDIATE (48): AI Agents (CrewAI, AutoGen), Voice Bots (AssemblyAI), 
Advanced RAG (Excel, Code, SQL routing), MCP integrations, Model comparisons

ADVANCED (23): Fine-tuning (DeepSeek, Unsloth), Reasoning models, Transformers from scratch,
Multi-Agent systems, NotebookLM clone, Production deployments

Tech Stack: CrewAI, LlamaIndex, Ollama, Qdrant, AssemblyAI, Groq, DeepSeek, Gemini, MCP
"""

def analyze():
    prompt = f"""Analyze this AI Engineering Hub and give:
1. Value Score (1-10)
2. Best 3 beginner projects
3. Best 3 advanced projects for career
4. Recommended learning path
5. Key strengths
6. One paragraph summary

{CONTENT}"""

    print("🤖 Analyzing with GPT-OSS-120B...\n")
    
    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1000
        },
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"]
        print("="*60)
        print("📊 AI ENGINEERING HUB ANALYSIS (GPT-OSS-120B)")
        print("="*60 + "\n")
        print(result)
        print("\n" + "="*60)
    else:
        print(f"❌ Error: {response.json()}")

if __name__ == "__main__":
    analyze()
