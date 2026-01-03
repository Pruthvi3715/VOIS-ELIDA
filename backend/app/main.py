from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse, StreamingResponse
from app.core.errors import AppException, ResourceNotFound, InvalidRequest, LLMGenerationError, AuthenticationError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
import asyncio
from typing import Optional, List
from sqlalchemy.orm import Session
from pydantic import BaseModel

load_dotenv()

from app.core.config import settings
from app.models.investor_dna import InvestorDNA, DEFAULT_INVESTOR_DNA
from app.orchestrator import orchestrator
from app.database import init_db, get_db, SessionLocal
from app.services.profile_service import profile_service
from app.services.history_service import history_service
from app.services.portfolio_service import portfolio_service
from app.auth.routes import router as auth_router
from app.auth.auth import get_current_user_id
from app.routers.profile import router as profile_router
from app.routers.history import router as history_router
from app.demo_cache import get_demo_analysis, is_demo_ticker, DEMO_ANALYSES

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""AI-Powered Investment Decision Support System
    
    Features:
    - Multi-agent AI analysis (Scout, Quant, Macro, Philosopher, Regret, Coach)
    - RAG-based knowledge base
    - Investor DNA matching system
    - Persistent Profiling & History
    - Portfolio scanning and analysis
    """,
    version="2.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Initialize database

# Global Exception Handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.code, 
            "message": exc.message
        }
    )

@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()

# Include routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(history_router)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to ELIDA - Financial Decision Support System API"}


@app.get("/health")
def health_check():
    llm_provider = os.getenv("LLM_PROVIDER", "auto")
    return {
        "status": "ok", 
        "version": "2.2", 
        "features": ["match_score", "investor_dna", "token_tracking", "authentication", "persistence"],
        "llm_provider": llm_provider
    }


# ============== LLM & Token Tracking Endpoints ==============

# Auth endpoints handled by auth_router

@app.get("/api/v1/auth/me")
def get_current_user(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    # Use profile service to fetch profile from DB
    profile_data = profile_service.get_profile_by_user_id(db, user_id)
    return {
        "user_id": user_id,
        "profile": profile_data
    }


# ============== LLM Parameters ==============

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


# ============== Portfolio Endpoints ==============

class PortfolioRequest(BaseModel):
    user_id: str
    tickers: List[str]

@app.post("/api/portfolio/scan")
def scan_portfolio(
    req: PortfolioRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Analyze multiple assets asynchronously.
    Returns a request_id to poll status.
    """
    try:
        user_id_int = int(req.user_id)
    except ValueError:
        # For MVP/Defaults, maybe handle differently, but service needs int
        # If user_id is "default", we can't save to DB easily per schema (ForeignKey).
        # We might need a default user in DB.
        if req.user_id == "default":
             # Hack: assume ID 1 is default or handle error
             # Better: raise error as portfolio feature requires login
             raise HTTPException(status_code=400, detail="Portfolio features require logged-in user")
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    request_id = portfolio_service.create_request(db, user_id_int, req.tickers)
    
    # Get profile snapshot
    profile_dict = profile_service.get_profile_by_user_id(db, req.user_id)
    profile = InvestorDNA(**profile_dict)
    
    # Launch background task
    background_tasks.add_task(
        portfolio_service.process_portfolio_async,
        SessionLocal,
        request_id,
        user_id_int,
        req.tickers,
        profile
    )
    
    return {
        "request_id": request_id,
        "status": "pending",
        "message": "Analysis started in background. Poll status endpoint for updates."
    }

@app.get("/api/portfolio/status/{request_id}")
def get_portfolio_status(request_id: str, db: Session = Depends(get_db)):
    """Get status of a portfolio analysis request."""
    status = portfolio_service.get_status(db, request_id)
    if not status:
        raise HTTPException(status_code=404, detail="Request not found")
    return status


# ============== Asset Analysis Endpoints ==============

@app.post("/ingest/{asset_id}")
def ingest_asset(asset_id: str, request: Request, user_id: str = Depends(get_current_user_id)):
    """Ingest asset data into RAG knowledge base."""
    return orchestrator.ingest_asset(asset_id)

def get_current_user_optional(user_id: str = "default"):
    """
    Dependency to get optional user ID.
    Ideally this should verify token but allow failure.
    For now, reusing the simple logic or placeholder.
    """
    # TODO: Implement proper optional auth
    return user_id

@app.get("/retrieve")
def retrieve(
    query: str, 
    asset_id: str, 
    user_id: str = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Retrieve analysis for an asset.
    """
    # Get user's profile
    profile_dict = profile_service.get_profile_by_user_id(db, user_id)
    profile = InvestorDNA(**profile_dict)
    
    result = orchestrator.retrieve_context(
        query=query,
        asset_id=asset_id,
        investor_dna=profile
    )
    
    # Save to History
    try:
        uid = int(user_id)
        history_service.save_entry(
            db=db,
            user_id=uid, 
            query_type="analysis", 
            query=asset_id, 
            result=result
        )
    except ValueError:
        pass
    
    return result

@app.get("/market-data/{asset_id}")
def get_market_data(asset_id: str, force_live: bool = True):
    """
    Fast endpoint: Get only market data.
    By default fetches live data from Yahoo Finance.
    Falls back to demo cache if live fetch fails.
    """
    from app.agents.scout import scout_agent
    
    try:
        # Always try live data first for real-time prices
        data = scout_agent.collect_data(asset_id)
        financials = data.get("financials", {})
        
        # Extract key market data with live prices
        price = financials.get("current_price", 0)
        prev_close = financials.get("previous_close", 0)
        
        # Calculate change percentage
        if prev_close and prev_close > 0:
            change_pct = ((price - prev_close) / prev_close) * 100
        else:
            change_pct = 0
        
        # Determine currency from ticker suffix
        currency = financials.get("currency", "USD")
        if asset_id.upper().endswith('.NS') or asset_id.upper().endswith('.BO'):
            currency = "INR"
        
        return {
            "price": price,
            "change": round(change_pct, 2),
            "volume": financials.get("volume") or data.get("technicals", {}).get("volume", 0),
            "high52w": financials.get("52_week_high"),
            "low52w": financials.get("52_week_low"),
            "pe_ratio": financials.get("pe_ratio"),
            "market_cap": financials.get("market_cap"),
            "currency": currency,
            "company_name": financials.get("company_name", asset_id),
            "source": "live"
        }
    except Exception as e:
        print(f"[Market Data] Live fetch failed for {asset_id}: {e}")
        # Fallback to demo cache
        demo = get_demo_analysis(asset_id)
        if demo:
            market_data = demo.get("market_data", {})
            market_data["source"] = "demo_cache"
            return market_data
        
        # Return error state
        return {
            "price": 0,
            "change": 0,
            "volume": 0,
            "currency": "INR" if asset_id.upper().endswith('.NS') else "USD",
            "error": str(e),
            "source": "error"
        }


@app.get("/analyze/{asset_id}")
def analyze_asset(
    asset_id: str, 
    demo: bool = False,
    user_id: str = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    One-shot analysis: Ingest + Retrieve in a single call.
    Use demo=true for instant cached results (hackathon demo mode).
    """
    if demo or is_demo_ticker(asset_id):
        demo_result = get_demo_analysis(asset_id)
        if demo_result:
            return demo_result
    
    profile_dict = profile_service.get_profile_by_user_id(db, user_id)
    profile = InvestorDNA(**profile_dict)
    
    orchestrator.ingest_asset(asset_id)
    
    result = orchestrator.retrieve_context(
        query="comprehensive analysis",
        asset_id=asset_id,
        investor_dna=profile
    )

    # Auto-save disabled per user request - manual save only
    # try:
    #     uid = int(user_id)
    #     history_service.save_entry(
    #         db=db,
    #         user_id=uid, 
    #         query_type="analysis", 
    #         query=asset_id, 
    #         result=result
    #     )
    # except ValueError:
    #     pass
    
    return result


@app.get("/api/demo/tickers")
def get_demo_tickers():
    """Get list of available demo tickers for instant analysis."""
    return {
        "tickers": list(DEMO_ANALYSES.keys()),
        "display_names": [t.replace(".NS", "") for t in DEMO_ANALYSES.keys()]
    }


@app.get("/api/compare")
def compare_stocks(
    tickers: str,
    db: Session = Depends(get_db)
):
    """
    Compare multiple stocks side by side.
    tickers: comma-separated list (e.g., "TCS.NS,INFY.NS")
    """
    ticker_list = [t.strip() for t in tickers.split(",")]
    results = {}
    
    for ticker in ticker_list[:4]:
        demo = get_demo_analysis(ticker)
        if demo:
            results[ticker] = {
                "ticker": ticker,
                "match_score": demo["match_score"],
                "verdict": demo["coach_verdict"]["verdict"],
                "confidence": demo["coach_verdict"]["confidence"],
                "summary": demo["match_result"]["summary"],
                "market_data": demo["market_data"],
                "breakdown": demo["match_result"]["breakdown"],
                "fit_reasons": demo["match_result"]["fit_reasons"][:2],
                "concern_reasons": demo["match_result"]["concern_reasons"][:2]
            }
        else:
            results[ticker] = {
                "ticker": ticker,
                "error": "Not a demo ticker - use demo tickers for instant comparison"
            }
    
    return {"comparison": results, "tickers": ticker_list}


AGENT_STAGES = [
    {"name": "Scout Agent", "description": "Collecting market data & news", "duration": 3},
    {"name": "Quant Agent", "description": "Analyzing fundamentals", "duration": 4},
    {"name": "Macro Agent", "description": "Evaluating economic indicators", "duration": 3},
    {"name": "Philosopher Agent", "description": "Assessing business quality", "duration": 4},
    {"name": "Regret Agent", "description": "Simulating risk scenarios", "duration": 3},
    {"name": "Coach Agent", "description": "Synthesizing final verdict", "duration": 2},
]

@app.get("/api/analyze-stream/{asset_id}")
async def analyze_stream(asset_id: str):
    """
    SSE endpoint for real-time agent progress during analysis.
    Returns demo data but simulates agent progress for demo effect.
    """
    async def generate():
        demo_result = get_demo_analysis(asset_id)
        
        for i, stage in enumerate(AGENT_STAGES):
            event_data = {
                "type": "agent_update",
                "agent": stage["name"],
                "status": "running",
                "description": stage["description"],
                "progress": int((i / len(AGENT_STAGES)) * 100)
            }
            yield f"data: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(0.5 if demo_result else stage["duration"])
            
            complete_data = {
                "type": "agent_complete",
                "agent": stage["name"],
                "status": "complete",
                "progress": int(((i + 1) / len(AGENT_STAGES)) * 100)
            }
            yield f"data: {json.dumps(complete_data)}\n\n"
        
        if demo_result:
            final_data = {"type": "complete", "result": demo_result}
        else:
            final_data = {"type": "complete", "result": {"error": "Use demo tickers for streaming demo"}}
        
        yield f"data: {json.dumps(final_data)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )


# ============== Utility Endpoints ==============

@app.get("/api/v1/rag/stats")
def get_rag_stats():
    """Get RAG knowledge base statistics."""
    from app.services.rag_service import rag_service
    return rag_service.get_stats()


@app.post("/chat/general")
async def general_chat(request: dict, db: Session = Depends(get_db)):
    """
    Handle general queries using Wikipedia and Web Scraping.
    """
    query = request.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    # TODO: Get user_id from request if available
    user_id_str = request.get("user_id", "default")
    
    answer = ""
    
    # -1. Try Qwen/Ollama (Local LLM)
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
            timeout=30 
        )
        
        if resp.status_code == 200:
            qwen_response = resp.json().get("response", "").strip()
            if "SEARCH_REQUIRED" not in qwen_response and len(qwen_response) > 10:
                answer = qwen_response
                
    except Exception as e:
        print(f"Qwen error: {e}")
    
    # 0. Try Gemini API 
    if not answer:
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-2.0-flash-exp') 
                
                # Contextual prompt
                prompt = f"""
                You are a helpful financial assistant named ELIDA. 
                Answer the following query concisely and accurately. 
                If it's a financial term, explain it simply.
                
                Query: {query}
                """
                response = model.generate_content(prompt)
                if response.text:
                    answer = response.text
                    # Save to History (Gemini)
                    try:
                        uid = int(user_id_str)
                        history_service.save_entry(
                            db=db,
                            user_id=uid,
                            query_type="search",
                            query=query,
                            result={"response": answer}
                        )
                    except ValueError:
                        pass
                    return {"response": answer}

            except Exception as e:
                print(f"Gemini error: {e}")

    # 1. Try Wikipedia 
    if not answer:
        try:
            import wikipedia
            try:
                answer = wikipedia.summary(query, sentences=4)
            except wikipedia.exceptions.DisambiguationError as e:
                answer = wikipedia.summary(e.options[0], sentences=4)
            except wikipedia.exceptions.PageError:
                search_results = wikipedia.search(query, results=1)
                if search_results:
                    answer = wikipedia.summary(search_results[0], sentences=4)
            
            if answer:
                import re
                answer = re.sub(r'\[\d+\]', '', answer)
                answer = re.sub(r'\b([A-Za-z]+)\s*=\s*([A-Za-z]+)\s*/\s*([A-Za-z]+)\b', r'$ \1 = \\frac{\2}{\3} $', answer)
                answer = answer.replace("=", " = ")

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
                snippet_classes = ["hgKElc", "V3FYCf", "BNeawe", "LGOjhe", "Z0LcW", "wx62f"]
                for cls in snippet_classes:
                    element = soup.find(class_=cls)
                    if element:
                        answer = element.get_text()
                        break
                if not answer:
                    results = soup.select("div.g")
                    if results:
                        answer = results[0].get_text()[:400] + "..."
        except Exception as e:
            print(f"Scraper error: {e}")

    if not answer:
        return {"response": f"I couldn't find a clear answer for '{query}' in my internal knowledge base."}
         
    # Formatting
    first_period = answer.find('.')
    if first_period > 0:
        import re
        first_sentence = answer[:first_period]
        match = re.search(r'^(.*?)\s+(is|refers to|defined as|measure of)\s', first_sentence, re.IGNORECASE)
        if match:
             subject = match.group(1)
             answer = answer.replace(subject, f"**{subject}**", 1)

    return {"response": answer}
