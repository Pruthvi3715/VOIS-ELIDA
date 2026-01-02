from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

from app.core.config import settings
from app.models.investor_dna import InvestorDNA, DEFAULT_INVESTOR_DNA
from app.orchestrator import orchestrator

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8501",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory profile storage (use database in production)
user_profiles: dict = {
    "default": DEFAULT_INVESTOR_DNA
}


@app.get("/")
def root():
    return {"message": "Welcome to ELIDA - Financial Decision Support System API"}


@app.get("/health")
def health_check():
    llm_provider = os.getenv("LLM_PROVIDER", "auto")
    return {
        "status": "ok", 
        "version": "2.1", 
        "features": ["match_score", "investor_dna", "token_tracking"],
        "llm_provider": llm_provider
    }


# ============== LLM & Token Tracking Endpoints ==============

@app.get("/api/v1/llm/config")
def get_llm_config():
    """Get current LLM configuration."""
    return {
        "provider": os.getenv("LLM_PROVIDER", "auto"),
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        "ollama_model": os.getenv("OLLAMA_MODEL", "llama3.1:latest")
    }


@app.get("/api/v1/llm/tokens")
def get_token_usage():
    """Get token usage statistics for all agents."""
    from app.agents.base import BaseAgent
    return BaseAgent.get_token_usage()


@app.post("/api/v1/llm/tokens/reset")
def reset_token_usage():
    """Reset token usage counters."""
    from app.agents.base import BaseAgent
    BaseAgent.reset_token_usage()
    return {"status": "ok", "message": "Token counters reset"}


# ============== Investor DNA Profile Endpoints ==============

@app.get("/api/v1/profile/{user_id}")
def get_profile(user_id: str):
    """Get investor DNA profile for a user."""
    if user_id in user_profiles:
        return {"profile": user_profiles[user_id].model_dump()}
    return {"profile": DEFAULT_INVESTOR_DNA.model_dump()}


@app.post("/api/v1/profile")
def create_or_update_profile(profile: InvestorDNA):
    """Create or update investor DNA profile."""
    user_profiles[profile.user_id] = profile
    return {
        "status": "success",
        "message": f"Profile updated for {profile.user_id}",
        "profile": profile.model_dump()
    }


@app.delete("/api/v1/profile/{user_id}")
def delete_profile(user_id: str):
    """Delete investor profile."""
    if user_id in user_profiles and user_id != "default":
        del user_profiles[user_id]
        return {"status": "success", "message": f"Profile deleted for {user_id}"}
    raise HTTPException(status_code=404, detail="Profile not found or cannot delete default")


# ============== Asset Analysis Endpoints ==============

# ... imports
from app.services.history_service import history_service
from pydantic import BaseModel
from typing import List

# ...

# ============== History & Portfolio Endpoints ==============

@app.get("/api/history/{user_id}")
def get_user_history(user_id: str):
    """Get recent history for a user."""
    return history_service.get_user_history(user_id)

@app.get("/api/history/item/{entry_id}")
def get_history_item(entry_id: str):
    """Get full result for a history item."""
    item = history_service.get_entry(entry_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

class PortfolioRequest(BaseModel):
    user_id: str
    tickers: List[str]

@app.post("/api/portfolio/scan")
def scan_portfolio(req: PortfolioRequest):
    """
    Analyze multiple assets and return consolidated verdicts.
    This is a simplified scan that runs the Orchestrator for each.
    """
    profile = user_profiles.get(req.user_id, DEFAULT_INVESTOR_DNA)
    results = []
    
    for ticker in req.tickers:
        ticker = ticker.strip()
        if not ticker: continue
        
        try:
            # 1. Reuse Orchestrator (Assuming fast enough or we'd need async BG tasks)
            # For MVP, we run sequential or simplified
            
            # Start with retrieval directly (assuming ingest happens lazily or already done)
            # To be safe, we do quick ingest
            orchestrator.ingest_asset(ticker)
            
            analysis = orchestrator.retrieve_context(
                query="verdict",
                asset_id=ticker,
                investor_dna=profile
            )
            
            # Extract high-level metrics
            match_res = analysis.get("match_result", {})
            results.append({
                "ticker": ticker,
                "score": match_res.get("score", 0),
                "recommendation": match_res.get("recommendation", "N/A"),
                "risk": match_res.get("risk_assessment", {}).get("risk_level", "Unknown")
            })

            # Save to History
            history_service.save_entry(
                user_id=req.user_id, 
                query_type="analysis", 
                query=ticker, 
                result=analysis
            )
            
        except Exception as e:
            results.append({
                "ticker": ticker,
                "error": str(e)
            })
            
    return {"results": results}

# ============== Asset Analysis Endpoints ==============

@app.post("/ingest/{asset_id}")
def ingest_asset(asset_id: str):
    """Ingest asset data into RAG knowledge base."""
    return orchestrator.ingest_asset(asset_id)

@app.get("/retrieve")
def retrieve(query: str, asset_id: str, user_id: Optional[str] = "default"):
    """
    Retrieve analysis for an asset.
    Optionally pass user_id to use their Investor DNA profile for Match Score.
    """
    # Get user's profile
    profile = user_profiles.get(user_id, DEFAULT_INVESTOR_DNA)
    
    result = orchestrator.retrieve_context(
        query=query,
        asset_id=asset_id,
        investor_dna=profile
    )
    
    # Save to History
    history_service.save_entry(
        user_id=user_id, 
        query_type="analysis", 
        query=asset_id, # Use asset_id (Ticker) as the query label
        result=result
    )
    
    return result

@app.get("/market-data/{asset_id}")
def get_market_data(asset_id: str):
    """
    Fast endpoint: Get only market data (Price, Financials, Technicals) without AI agents.
    Used for quick UI rendering before deep analysis.
    """
    from app.agents.scout import scout_agent
    return scout_agent.collect_data(asset_id)


@app.get("/analyze/{asset_id}")
def analyze_asset(asset_id: str, user_id: Optional[str] = "default"):
    """
    One-shot analysis: Ingest + Retrieve in a single call.
    """
    # Get user's profile
    profile = user_profiles.get(user_id, DEFAULT_INVESTOR_DNA)
    
    # Ingest
    orchestrator.ingest_asset(asset_id)
    
    # Analyze
    result = orchestrator.retrieve_context(
        query="comprehensive analysis",
        asset_id=asset_id,
        investor_dna=profile
    )

    # Save to History
    history_service.save_entry(
        user_id=user_id, 
        query_type="analysis", 
        query=asset_id, 
        result=result
    )
    
    return result


# ============== Utility Endpoints ==============

@app.get("/api/v1/rag/stats")
def get_rag_stats():
    """Get RAG knowledge base statistics."""
    from app.services.rag_service import rag_service
    return rag_service.get_stats()


@app.post("/chat/general")
async def general_chat(request: dict):
    """
    Handle general queries using Wikipedia and Web Scraping.
    Simulates AI knowledge without API keys.
    """
    query = request.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    answer = ""
    source = ""
    
    # -1. Try Qwen/Ollama (Local LLM) - REQUESTED PRIORITY
    ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    
    try:
        import requests
        print(f"Asking Qwen ({ollama_model})...")
        qwen_prompt = f"""You are a helpful financial assistant. Answer the following query concisely.
If the query requires real-time data (like current stock price) or if you honestly don't know, respond with exactly: SEARCH_REQUIRED

Query: {query}"""
        
        resp = requests.post(
            ollama_url, 
            json={
                "model": ollama_model, 
                "prompt": qwen_prompt, 
                "stream": False,
                "options": {"temperature": 0.3}
            },
            timeout=30 # Quick timeout for local
        )
        
        if resp.status_code == 200:
            qwen_response = resp.json().get("response", "").strip()
            print(f"Qwen response: {qwen_response[:50]}...")
            
            if "SEARCH_REQUIRED" not in qwen_response and len(qwen_response) > 10:
                # Successfully answered
                return {"response": qwen_response}
            else:
                print("Qwen requested search or insufficient answer.")
                
    except Exception as e:
        print(f"Qwen error: {e}")
    
    # 0. Try Gemini API (Smartest)
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp') # Or 1.5-flash
            
            # Contextual prompt
            prompt = f"""
            You are a helpful financial assistant named ELIDA. 
            Answer the following query concisely and accurately. 
            If it's a financial term, explain it simply.
            
            Query: {query}
            """
            response = model.generate_content(prompt)
            if response.text:
                result = {"response": response.text}
                # Save to History (Gemini)
                history_service.save_entry(
                    user_id="default", # TODO: Get from request
                    query_type="search",
                    query=query,
                    result=result
                )
                return result
        except Exception as e:
            print(f"Gemini error: {e}")
            # Fallthrough to Wiki
            
    # 1. Try Wikipedia (High quality definitions)
    try:
        import wikipedia
        # Limit to 3 sentences for concise "AI-like" answer
        try:
            # First try direct summary
            answer = wikipedia.summary(query, sentences=4)
        except wikipedia.exceptions.DisambiguationError as e:
            # If ambiguous, take the first option
            answer = wikipedia.summary(e.options[0], sentences=4)
        except wikipedia.exceptions.PageError:
            # If not found, search for terms and use first result
            search_results = wikipedia.search(query, results=1)
            if search_results:
                answer = wikipedia.summary(search_results[0], sentences=4)
        
        if answer:
            # Clean up artifacts like [1], [2]
            import re
            answer = re.sub(r'\[\d+\]', '', answer)
            
            # Formatting: Bold the query terms presence in the first sentence
            # Simple heuristic: Split query words, try to match them case-insensitive
            query_words = query.lower().split()
            # For each word, try to bold it in the text (first occurrence)
            # A better approach: Find the first sentence and bold the defining subject
            # E.g. "The **price-earnings ratio** (P/E ratio) is..."
            
            # Let's bold the first 5-8 words if they effectively repeat the title
            # Or just rely on finding the query string?
            # Let's try to bold the specific phrase "price-earnings ratio" if found
            
            # Custom formatter for formulas
            # Detect patterns like "ratio = Price / Earnings" or similar
            # Regex for "A = B / C"
            answer = re.sub(r'\b([A-Za-z]+)\s*=\s*([A-Za-z]+)\s*/\s*([A-Za-z]+)\b', r'$ \1 = \\frac{\2}{\3} $', answer)
            
            # General clean up
            answer = answer.replace("=", " = ") # Ensure spacing for readability if not caught
            
            # Rule 3 formatting: Use headers
            source = "Knowledge Base (Wiki)" # (This variable is now local, we don't output it per Rule 3)

    except Exception as e:
        print(f"Wiki error: {e}")
        
    # 2. Fallback to Google Search Scraping
    if not answer:
        try:
            import requests
            from bs4 import BeautifulSoup
            import urllib.parse
            
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # specific snippets
                snippet_classes = ["hgKElc", "V3FYCf", "BNeawe", "LGOjhe", "Z0LcW", "wx62f"]
                for cls in snippet_classes:
                    element = soup.find(class_=cls)
                    if element:
                        answer = element.get_text()
                        break
                        
                # Fallback to description
                if not answer:
                    results = soup.select("div.g")
                    if results:
                        answer = results[0].get_text()[:400] + "..."
        except Exception as e:
            print(f"Scraper error: {e}")

    if not answer:
        return {"response": f"I couldn't find a clear answer for '{query}' in my internal knowledge base."}
         
    # Apply formatting to the final answer if not done
    # Bold the first significant noun phrase? 
    # Let's bold the Subject of the first sentence.
    first_period = answer.find('.')
    if first_period > 0:
        first_sentence = answer[:first_period]
        # Heuristic: Bold everything before " is " or " refers to "
        match = re.search(r'^(.*?)\s+(is|refers to|defined as|measure of)\s', first_sentence, re.IGNORECASE)
        if match:
             subject = match.group(1)
             answer = answer.replace(subject, f"**{subject}**", 1)

    # Rule 3: Invisibility - Do not explain sources
    # Just return the direct answer
    return {"response": answer}
