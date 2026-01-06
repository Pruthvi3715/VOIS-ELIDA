# ELIDA - Technical Presentation Guide
## Quick Reference for Your Evaluation Meeting

---

## 🎯 PROJECT OVERVIEW (30 seconds)

**ELIDA** = Enhanced Learning Investment Decision Advisor

**One-liner:** "An AI-powered stock analysis system that uses multiple specialized agents to provide personalized investment recommendations."

**Unique Value:** Combines real-time market data + Multi-agent AI + Personalized Investor DNA matching.

---

## 🏗️ ARCHITECTURE AT A GLANCE

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│  React UI      │────▶│  FastAPI       │────▶│  AI Agents     │
│  (Port 5173)   │     │  (Port 8000)   │     │  (6 Agents)    │
└────────────────┘     └────────────────┘     └────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ChromaDB        SQLite          Yahoo Finance
        (RAG)          (Users)         (Market Data)
```

---

## 🤖 THE 6 AI AGENTS (KEY TALKING POINT!)

| Agent | Role | What It Analyzes | Output |
|-------|------|------------------|--------|
| 🔍 **Scout** | Data Collector | Fetches live data from Yahoo Finance | Price, Volume, News, Financials |
| 📊 **Quant** | Number Cruncher | P/E, ROE, Debt/Equity, Margins | Score 0-100 + Reasoning |
| 🌍 **Macro** | Market Context | VIX, Interest Rates, Sector Trends | Trend Analysis |
| 🧠 **Philosopher** | Quality Judge | Moat, Management, ESG | Ethics Score |
| ⚠️ **Regret** | Risk Simulator | Worst-case scenarios | Risk Level |
| 🎯 **Coach** | Synthesizer | All agent outputs + Investor DNA | Final BUY/HOLD/SELL |

**Key Technical Detail:** Agents run **sequentially** (not parallel) with 3-second delays to avoid API rate limits.

---

## 🧬 INVESTOR DNA FEATURE (UNIQUE SELLING POINT!)

**Concept:** The system creates a "DNA profile" of the investor based on:
- Risk Tolerance (Conservative → Aggressive)
- Investment Horizon (Short/Medium/Long term)
- Financial Goals (Growth, Income, Safety)
- Sectors to Avoid (e.g., Tobacco, Gambling)

**The Match Score:** 0-100 rating of how well a stock fits the investor's profile.

**Example:** An aggressive investor with 10-year horizon gets different recommendations than a conservative investor seeking safety.

---

## 🔄 ANALYSIS FLOW (How It Works)

1. User enters stock symbol (e.g., `TCS.NS` for Tata Consultancy)
2. **Scout Agent** collects data from Yahoo Finance
3. Data stored in **ChromaDB** (Vector Database for RAG)
4. 4 Analysis Agents run sequentially:
   - Quant → 3s delay → Macro → 3s delay → Philosopher → 3s delay → Regret
5. **Match Score** calculated against Investor DNA
6. **Coach Agent** synthesizes everything into final verdict
7. Results displayed + saved to history

**Time:** ~30-60 seconds for complete analysis

---

## 💻 TECH STACK DETAILS

### Frontend (React 19)
- **Framework:** React 19 + Vite
- **Styling:** Custom CSS (Dark theme with glass effects)
- **Key Pages:**
  - Dashboard (Live Market, Search)
  - Analysis Results (Agent Cards, Coach Verdict)
  - Profile (Investor DNA settings)
  - History (Past analyses)
  - Chat (AI assistant)

### Backend (FastAPI)
- **Language:** Python 3.11
- **Framework:** FastAPI (async, fast, auto-docs)
- **Key Endpoints:**
  - `GET /analyze/{ticker}` - Full analysis
  - `GET /market-data/{ticker}` - Live prices
  - `POST /chat/general` - Chatbot

### AI/LLM Layer
- **Current Provider:** Ollama (Local)
- **Model:** qwen2.5:7b
- **Fallback Options:** Groq, Gemini

### Data Storage
| Store | Tech | Purpose |
|-------|------|---------|
| RAG | ChromaDB | Embeddings for context retrieval |
| Users/History | SQLite | Persistent user data |
| Cache | In-Memory | API response caching |

---

## 🔐 AUTHENTICATION

- **Method:** JWT (JSON Web Tokens)
- **Flow:** Register → Login → Token → Authenticated requests
- **Token Expiry:** 24 hours

---

## 📊 KEY METRICS FOR DEMO

| Metric | Value |
|--------|-------|
| Analysis Time | 30-60 seconds |
| API Response | <500ms |
| Agents | 6 specialized |
| LLM Providers | 3 (Ollama, Groq, Gemini) |
| Match Score Range | 0-100 |

---

## 🚨 COMMON QUESTIONS & ANSWERS

### Q: Why multiple agents instead of one AI?
**A:** Each agent specializes in different analysis (like specialists in a hospital). Quant focuses on numbers, Philosopher on ethics, Regret on risks. This provides balanced, comprehensive analysis.

### Q: How is this different from ChatGPT?
**A:** ChatGPT is general-purpose. ELIDA:
- Fetches real-time market data
- Has specialized financial agents
- Provides personalized recommendations based on Investor DNA
- Scores and ranks stocks

### Q: What is RAG?
**A:** Retrieval-Augmented Generation. We store stock data in ChromaDB, then retrieve relevant context before asking the LLM. This gives accurate, data-backed responses.

### Q: Why Ollama instead of cloud LLMs?
**A:** Cloud LLMs (Groq, Gemini) have rate limits. Ollama runs locally with:
- No rate limits
- No API costs
- Works offline
- Handles large prompts

### Q: What's the Match Score?
**A:** A 0-100 rating of how well a stock fits the investor's profile. Above 70 = Good fit. Below 40 = Poor fit.

---

## 🎓 KEY TERMS TO KNOW

| Term | Definition |
|------|------------|
| **RAG** | Retrieval-Augmented Generation - adding context to LLM prompts |
| **ChromaDB** | Vector database for storing embeddings |
| **Investor DNA** | User's investment profile (risk, horizon, goals) |
| **Match Score** | 0-100 rating of stock-investor compatibility |
| **Orchestrator** | Central coordinator that manages all agents |
| **JWT** | JSON Web Token for secure authentication |

---

## ✅ PRE-PRESENTATION CHECKLIST

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Ollama running with qwen2.5:7b model
- [ ] Test one analysis before demo (e.g., TCS.NS)
- [ ] Login working
- [ ] History page showing data

---

## 🎯 DEMO FLOW SUGGESTION

1. **Show Dashboard** - Point out Live Market section
2. **Search for a stock** (e.g., RELIANCE.NS)
3. **Wait for analysis** - Explain agents are running
4. **Show Results** - Walk through each agent card
5. **Highlight Match Score** - Explain personalization
6. **Show Coach Verdict** - Final recommendation
7. **Show Investor DNA** - How personalization works
8. **Show History** - Past analyses saved

**Time:** ~3-5 minutes

---

## 📞 IF SOMETHING BREAKS

| Problem | Quick Fix |
|---------|-----------|
| "Analysis failed" | Restart backend: `python -m uvicorn app.main:app --reload --port 8000` |
| Slow response | Using local Ollama, takes 30-60s - this is normal |
| Rate limit errors | Already using Ollama, no rate limits |
| Frontend not loading | Check `npm run dev` in frontend folder |

---

**Good luck with your presentation! 🚀**

*Team 83 - MMIT, Pune*
