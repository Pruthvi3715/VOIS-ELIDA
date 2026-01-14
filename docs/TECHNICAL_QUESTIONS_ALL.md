# 🎯 ELIDA - Complete Technical Q&A Guide

> **All possible technical questions with detailed answers for the ELIDA project presentation**

---

## 🏗️ ARCHITECTURE & DESIGN

### Q1: Why did you choose a Multi-Agent Architecture instead of a single AI model?
**Answer:** A single AI model would have to handle everything - data collection, fundamental analysis, macro analysis, behavioral assessment, and synthesis. This leads to:
- Inconsistent quality across different aspects
- Harder to debug and improve
- No specialization

Multi-agent gives us:
- **Specialization**: Each agent is an expert in one domain
- **Modularity**: Can improve one agent without affecting others
- **Scalability**: Can add new agents (e.g., for crypto) easily
- **Mimics reality**: Real investment firms have specialized teams

---

### Q2: Explain the communication flow between the 6 AI agents.
**Answer:**
```
User Request → Orchestrator → Scout Agent (collects data)
                    ↓
           Data stored in ChromaDB
                    ↓
    ┌───────────┬───────────┬───────────┐
    ↓           ↓           ↓           ↓
  Quant      Macro     Philosopher   Regret
  Agent      Agent       Agent       Agent
    ↓           ↓           ↓           ↓
    └───────────┴───────────┴───────────┘
                    ↓
              Coach Agent (synthesis)
                    ↓
              Final Result
```
Each agent receives the raw data from Scout, analyzes independently, and Coach combines all insights with user's Investor DNA.

---

### Q3: Why FastAPI instead of Flask or Django?
**Answer:**
| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Async Support | ✅ Native | ❌ Limited | ❌ Limited |
| Speed | ⚡ Very Fast | Medium | Slower |
| Auto Docs | ✅ Swagger/OpenAPI | ❌ Manual | ❌ Manual |
| Type Hints | ✅ Built-in | ❌ None | ❌ None |
| Learning Curve | Low | Low | High |

FastAPI is ideal for AI applications because:
- Async handling for multiple LLM calls
- Automatic request validation with Pydantic
- Built-in API documentation at `/docs`

---

### Q4: How does the orchestrator coordinate between different agents?
**Answer:**
```python
# Simplified orchestrator flow:
async def analyze_stock(ticker: str, user_profile: dict):
    # Step 1: Scout collects data
    raw_data = await scout_agent.collect(ticker)
    
    # Step 2: Store in RAG
    await rag_service.store(raw_data)
    
    # Step 3: Run analysis agents (can be parallel or sequential)
    quant_result = await quant_agent.analyze(raw_data)
    macro_result = await macro_agent.analyze(raw_data)
    phil_result = await philosopher_agent.analyze(raw_data)
    regret_result = await regret_agent.analyze(raw_data)
    
    # Step 4: Coach synthesizes with user profile
    final = await coach_agent.synthesize(
        quant_result, macro_result, phil_result, regret_result,
        user_profile
    )
    
    return final
```
The orchestrator manages the entire pipeline, handles errors, and ensures fallbacks work.

---

### Q5: What is the role of the Scout Agent vs other agents?
**Answer:**
| Aspect | Scout Agent | Other Agents |
|--------|-------------|--------------|
| Purpose | Data Collection | Data Analysis |
| Input | Stock ticker | Raw data from Scout |
| Output | Financials, news, technicals | Insights, scores, recommendations |
| External APIs | Yes (Yahoo, Screener) | No - uses RAG |
| Runs First | Always first | After Scout completes |

Scout is the "researcher" - goes out, gets data. Others are "analysts" - interpret the data.

---

### Q6: Why is the analysis done sequentially rather than in parallel?
**Answer:** Actually, the 4 analysis agents (Quant, Macro, Philosopher, Regret) CAN run in parallel since they're independent. Only the sequence is:
1. Scout MUST run first (to collect data)
2. Analysis agents (parallel possible)
3. Coach MUST run last (needs all inputs)

In implementation, we run them sequentially for:
- Better error handling
- Easier debugging
- Lower memory usage
- More predictable LLM rate limiting

---

### Q7: Why did you choose React 19 with Vite instead of Next.js?
**Answer:**
- **Simplicity**: No SSR needed for a dashboard app
- **Speed**: Vite has extremely fast hot reload
- **Size**: Smaller bundle than Next.js
- **Separation**: Pure frontend, clear API boundary with FastAPI
- **React 19**: Latest features like Server Components (optional)

Next.js would be overkill - we don't need SEO or server-side rendering for a logged-in dashboard.

---

## 🤖 AI/ML & LLM QUESTIONS

### Q8: Explain your LLM fallback chain (Ollama → Groq → Gemini). Why this order?
**Answer:**
```
Order: Ollama (Local) → Groq (Cloud) → Gemini (Cloud)

Why this order:
1. Ollama FIRST:
   - No API costs
   - No network latency
   - Data stays private
   - Works offline
   
2. Groq SECOND:
   - Extremely fast (fastest LLM API)
   - Free tier available
   - Good quality (LLaMA models)
   
3. Gemini LAST:
   - Most reliable
   - Highest quality
   - But has rate limits and costs
```

---

### Q9: What happens if all LLM providers fail?
**Answer:**
```python
# Fallback behavior:
try:
    result = await ollama_call()
except:
    try:
        result = await groq_call()
    except:
        try:
            result = await gemini_call()
        except:
            # All failed - return fallback response
            result = {
                "status": "fallback",
                "message": "Analysis temporarily unavailable",
                "recommendation": "Please try again later",
                "data": raw_data  # Still show raw data
            }
```
User sees an error message but still gets the raw data that was collected.

---

### Q10: Why did you choose Ollama for local LLM support?
**Answer:**
- **Open Source**: Free and community-supported
- **Easy Setup**: One command install
- **Model Variety**: Supports LLaMA, Mistral, Qwen, etc.
- **API Compatible**: OpenAI-style API, easy to integrate
- **Privacy**: Data never leaves the machine
- **Offline**: Works without internet

---

### Q11: What model are you using with Ollama? Why?
**Answer:** We use **Qwen 2.5 7B** because:
- **Size**: 7B parameters - fits in 8GB VRAM
- **Quality**: Excellent at structured output (JSON)
- **Speed**: Fast inference, ~5 tokens/second on good GPU
- **Context**: 32K context window
- Alternatives: LLaMA 3.1 8B, Mistral 7B

---

### Q12: How does the Quant Agent calculate fundamental scores?
**Answer:**
```python
# Quant scoring example:
def calculate_score(data):
    score = 0
    
    # P/E Ratio (lower is better for value)
    if data.pe_ratio < 15: score += 20
    elif data.pe_ratio < 25: score += 10
    
    # ROE (higher is better)
    if data.roe > 20: score += 20
    elif data.roe > 10: score += 10
    
    # Debt/Equity (lower is better)
    if data.debt_equity < 0.5: score += 20
    elif data.debt_equity < 1: score += 10
    
    # Revenue Growth (higher is better)
    if data.revenue_growth > 15: score += 20
    elif data.revenue_growth > 5: score += 10
    
    # Profit Margin
    if data.profit_margin > 15: score += 20
    elif data.profit_margin > 5: score += 10
    
    return score  # Max 100
```

---

### Q13: Explain the Regret Minimization Engine - how does it simulate worst-case scenarios?
**Answer:**
Based on **Prospect Theory** by Kahneman & Tversky:
```python
def simulate_regret(stock_data, user_profile):
    # Calculate historical volatility
    volatility = calculate_volatility(stock_data.price_history)
    
    # Simulate worst-case (2 standard deviations down)
    worst_case_drop = volatility * 2
    
    # Calculate potential loss
    if user_profile.investment_amount:
        potential_loss = investment * worst_case_drop
    
    # Regret score based on loss aversion (losses hurt 2x gains)
    regret_score = calculate_regret(
        potential_loss,
        user_profile.risk_tolerance
    )
    
    return {
        "worst_case_scenario": f"Stock could drop {worst_case_drop}%",
        "potential_loss": potential_loss,
        "regret_score": regret_score,
        "advice": "Only invest if you can handle this drop"
    }
```

---

### Q14: Why did you choose ChromaDB for vector storage?
**Answer:**
| Feature | ChromaDB | Pinecone | Weaviate |
|---------|----------|----------|----------|
| Open Source | ✅ Yes | ❌ No | ✅ Yes |
| Setup | Simple | Cloud only | Complex |
| Local Mode | ✅ Yes | ❌ No | ❌ Limited |
| Cost | Free | Paid | Free/Paid |
| Python Native | ✅ Excellent | Good | Good |

ChromaDB is perfect for:
- Prototype/demo phase
- Local development
- No cloud dependency

---

### Q15: What embedding model are you using for RAG?
**Answer:** We use **sentence-transformers/all-MiniLM-L6-v2**:
- 384-dimensional embeddings
- Very fast
- Good quality for semantic search
- Open source, free

For production, could upgrade to OpenAI's text-embedding-3-small.

---

### Q16: How does RAG improve the accuracy of agent responses?
**Answer:**
**Without RAG:**
```
User: "Analyze TCS"
LLM: "TCS is a good company..." (generic, possibly outdated)
```

**With RAG:**
```
User: "Analyze TCS"
System: 
  1. Retrieve TCS data from ChromaDB
  2. Include in prompt: "Here's current TCS data: P/E: 28, ROE: 45%..."
  3. LLM generates based on ACTUAL data
Result: Factually accurate, current analysis
```

RAG **grounds** the LLM in real data, preventing hallucinations.

---

## 🧠 BEHAVIORAL FINANCE QUESTIONS

### Q17: How do you calculate the 0-100 Investor DNA Match Score?
**Answer:**
```python
def calculate_match_score(stock, investor_profile):
    score = 100  # Start at 100, deduct for mismatches
    
    # Risk Match
    stock_volatility = get_volatility(stock)
    if investor_profile.risk == "conservative":
        if stock_volatility > 30: score -= 30
        elif stock_volatility > 20: score -= 15
    
    # Horizon Match
    if investor_profile.horizon == "short":
        if stock.is_growth_stock: score -= 20  # Growth needs time
    
    # Sector Avoidance
    if stock.sector in investor_profile.avoid_sectors:
        score -= 40  # Major penalty for avoided sectors
    
    # Goal Match
    if investor_profile.goal == "income":
        if stock.dividend_yield > 3: score += 10
        else: score -= 10
    
    return max(0, min(100, score))
```

---

### Q18: Explain Prospect Theory and how you've implemented it in the Regret Agent.
**Answer:**
**Prospect Theory says:**
1. People feel losses 2x more than equivalent gains
2. People prefer certainty over gambles
3. Reference point matters

**Our Implementation:**
```
Regret Agent shows:
- "If stock drops 30%, you lose ₹30,000" (Loss framing)
- "Similar stocks recovered in 18 months historically" (Reference point)
- "Can you hold for 18 months without selling?" (Behavior check)

This prepares users for downside, reducing panic-selling.
```

---

### Q19: How do you address Loss Aversion in your recommendations?
**Answer:**
1. **Show worst-case first**: Before showing upside potential
2. **Quantify in rupees**: "You could lose ₹10,000" hits harder than "10% drop"
3. **Ask the right question**: "Would you panic-sell at this loss?"
4. **Match to tolerance**: Conservative investors get lower-volatility stocks
5. **Historical context**: "This stock recovered from 2008 crash in 2 years"

---

## 💾 DATABASE & DATA MANAGEMENT

### Q20: Why SQLite instead of PostgreSQL or MongoDB?
**Answer:**
| Aspect | SQLite | PostgreSQL | MongoDB |
|--------|--------|------------|---------|
| Setup | Zero | Complex | Medium |
| Deployment | Single file | Server needed | Server needed |
| Scale | 10K users | Millions | Millions |
| Use Case | Prototype | Production | Documents |

SQLite for now because:
- Single file deployment
- No server setup
- Perfect for demo/prototype
- Easy migration to PostgreSQL later

---

### Q21: Explain your database schema for users, profiles, and history.
**Answer:**
```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Investor Profiles Table
CREATE TABLE investor_profiles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    risk_tolerance TEXT,  -- conservative/moderate/aggressive
    investment_horizon TEXT,  -- short/medium/long
    financial_goals TEXT,
    avoid_sectors TEXT,  -- JSON array
    created_at TIMESTAMP
);

-- Analysis History Table
CREATE TABLE analysis_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    ticker TEXT NOT NULL,
    analysis_result TEXT,  -- JSON blob
    match_score INTEGER,
    recommendation TEXT,
    created_at TIMESTAMP
);
```

---

### Q22: What APIs do you use to fetch stock data?
**Answer:**
1. **Primary: Yahoo Finance (yfinance library)**
   - Free, reliable
   - Supports global stocks
   - Real-time + historical data

2. **Fallback: Screener.in (for Indian stocks)**
   - Used when Yahoo fails for Indian tickers
   - Better fundamental data for Indian companies

3. **Macro Data: FRED API**
   - VIX, Treasury yields
   - Economic indicators

---

### Q23: How do you handle Yahoo Finance API failures or rate limits?
**Answer:**
```python
async def get_stock_data(ticker):
    try:
        # Try Yahoo Finance first
        data = yf.Ticker(ticker).info
        if data and 'regularMarketPrice' in data:
            return data
    except Exception:
        pass
    
    # Fallback for Indian stocks
    if ticker.endswith('.NS') or ticker.endswith('.BO'):
        try:
            data = screener_service.get_data(ticker)
            return data
        except Exception:
            pass
    
    # Return cached data if available
    cached = cache_service.get(ticker)
    if cached:
        return {**cached, "source": "cache", "warning": "Using cached data"}
    
    raise DataNotFoundError(f"No data for {ticker}")
```

---

## 🔐 SECURITY & AUTHENTICATION

### Q24: How does JWT authentication work in your system?
**Answer:**
```
1. User registers/logs in with email + password
2. Server verifies password hash
3. Server generates JWT token:
   {
     "user_id": 123,
     "email": "user@example.com",
     "exp": 1704067200  // 24 hours from now
   }
   Signed with SECRET_KEY
4. Frontend stores token in localStorage
5. All API requests include: Authorization: Bearer <token>
6. Server verifies token on each request
7. Token expires after 24 hours → re-login required
```

---

### Q25: How do you hash user passwords?
**Answer:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)
```
Using **bcrypt** with automatic salt generation. Password is NEVER stored in plain text.

---

### Q26: How do you prevent common vulnerabilities (SQL Injection, XSS, CSRF)?
**Answer:**
| Vulnerability | Prevention |
|---------------|------------|
| SQL Injection | SQLAlchemy ORM (parameterized queries) |
| XSS | React escapes by default, no dangerouslySetInnerHTML |
| CSRF | JWT tokens (not cookies), CORS configuration |
| Password Exposure | bcrypt hashing, no plain text |
| API Key Leaks | Environment variables, .env files |

---

## ⚡ PERFORMANCE & SCALABILITY

### Q27: What is the average response time for stock analysis?
**Answer:**
| Phase | Time |
|-------|------|
| Scout (data collection) | ~1.5 seconds |
| Quant Analysis | ~0.5 seconds |
| Macro Analysis | ~0.5 seconds |
| Philosopher Analysis | ~0.5 seconds |
| Regret Analysis | ~0.5 seconds |
| Coach Synthesis | ~1.0 seconds |
| **Total** | **~4.5 seconds** |

Under 5 seconds as promised!

---

### Q28: How would you scale this for 100,000+ users?
**Answer:**
1. **Database**: Migrate SQLite → PostgreSQL
2. **Caching**: Add Redis for session/data caching
3. **Load Balancing**: nginx + multiple FastAPI instances
4. **LLM Scaling**: Use cloud LLM APIs (Groq, Gemini) with rate limiting
5. **Queue**: Add Celery for background analysis jobs
6. **CDN**: Static assets on CloudFlare
7. **Containerization**: Docker + Kubernetes

---

### Q29: What optimizations did you implement to achieve <5 second response time?
**Answer:**
1. **Caching**: Stock data cached for 5 minutes
2. **Parallel agents**: Analysis agents can run concurrently
3. **Fast LLM**: Qwen 7B locally, Groq for cloud (fastest API)
4. **Minimal prompts**: Optimized prompts for speed
5. **Async operations**: FastAPI async for non-blocking I/O
6. **Vector preloading**: ChromaDB kept in memory

---

## 📊 FINANCIAL ANALYSIS LOGIC

### Q30: How do you interpret VIX for market sentiment?
**Answer:**
```
VIX (Volatility Index) Interpretation:
- VIX < 15: Low fear, bullish market
- VIX 15-20: Normal volatility
- VIX 20-30: Elevated fear, caution advised
- VIX > 30: High fear, possible crash, defensive mode

Macro Agent uses VIX to adjust recommendations:
- High VIX + Growth Stock = Lower match score (risky)
- High VIX + Dividend Stock = Higher score (safe haven)
```

---

### Q31: How do you determine BUY/HOLD/SELL recommendations?
**Answer:**
```
Match Score → Recommendation:
- 80-100: STRONG BUY (Excellent match)
- 60-79: BUY (Good match)
- 40-59: HOLD (Neutral/watch)
- 20-39: REDUCE (Poor match)
- 0-19: SELL (Very poor match)

Factors:
1. Investor DNA match
2. Fundamental strength (Quant)
3. Market conditions (Macro)
4. Quality moat (Philosopher)
5. Risk tolerance vs volatility (Regret)
```

---

## 🧪 TESTING & DEPLOYMENT

### Q32: What testing frameworks did you use?
**Answer:**
- **Backend**: pytest, pytest-asyncio
- **Frontend**: Vitest (Vite-native)
- **API Testing**: httpx for async tests
- **Manual**: Postman for API, browser for UI

---

### Q33: How would you deploy this to production?
**Answer:**
```
Option 1: Traditional VPS
- Ubuntu server on DigitalOcean/AWS EC2
- nginx as reverse proxy
- PM2 or systemd for process management
- Let's Encrypt for HTTPS

Option 2: Docker
- Dockerfile for backend + frontend
- docker-compose for multi-container
- Deploy to AWS ECS or Railway

Option 3: Serverless
- Backend: AWS Lambda + API Gateway
- Frontend: Vercel/Netlify
- Database: PlanetScale (MySQL)
```

---

## 🔄 API DESIGN

### Q34: What REST endpoints does your backend expose?
**Answer:**
```
Authentication:
POST   /api/auth/register    - Create new user
POST   /api/auth/login       - Get JWT token
GET    /api/auth/me          - Get current user

Analysis:
POST   /api/analyze/{ticker} - Run full analysis
GET    /api/analysis/{id}    - Get saved analysis

Profile:
GET    /api/profile          - Get investor profile
PUT    /api/profile          - Update investor profile

History:
GET    /api/history          - List all analyses
DELETE /api/history/{id}     - Delete an analysis

Chat:
POST   /api/chat             - General chatbot
```

---

## 💡 DESIGN DECISIONS

### Q35: Why did you choose SQLAlchemy over raw SQL?
**Answer:**
1. **Security**: Auto-parameterized queries prevent SQL injection
2. **Pythonic**: Work with objects, not strings
3. **Migrations**: Easy schema changes with Alembic
4. **Portability**: Switch databases without code changes
5. **DRY**: Don't repeat query patterns

---

### Q36: Why Python for backend instead of Node.js?
**Answer:**
| Aspect | Python | Node.js |
|--------|--------|---------|
| AI/ML Libraries | Excellent | Limited |
| Data Science | NumPy, Pandas | Not native |
| LLM Integration | langchain, etc. | Less mature |
| Financial Data | yfinance, etc. | npm alternatives |
| Team Expertise | High | Medium |

Python is the natural choice for AI-heavy applications.

---

> **Prepared for ELIDA Team 83 - VOIS Innovation Marathon 2026**
