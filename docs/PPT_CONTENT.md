# ELIDA - PPT Content Following VOIS Template Format
## (Copy this content into your VOIS_ProjectPresentationTemplate_2025.pptx)

---

## SLIDE 1: Title Slide

**Project Title:** ELIDA - AI Investment Decision Advisor

**Team Number:** 83

**Team Members:**
- Pruthviraj Shinde
- Kinjal Jadhav
- Siddanth Lokhnade

**Project Mentor:** Deepneel Majumdar

**College:** Maharashtra Institute of Management, Information Technology (MMIT), Loni Kalbhor, Pune

**Semester:** 3 | **Year:** 2025-26

---

## SLIDE 2: Problem Statement

### The Problem
Young retail investors face significant challenges when making investment decisions:

1. **Information Overload** - Too many data sources, contradicting opinions
2. **Lack of Expertise** - Complex financial metrics (P/E, ROE, Debt ratios) are hard to understand
3. **Emotional Bias** - Fear and greed lead to poor timing decisions
4. **No Personalization** - Generic advice doesn't match individual risk profiles
5. **High Advisory Costs** - Professional advice is expensive and inaccessible

### Impact
- 70% of retail investors lose money in their first year
- Over 10 crore Demat accounts in India with most being new investors

---

## SLIDE 3: Objectives

### Project Objectives

1. **Build Multi-Agent AI System**
   - Create specialized AI agents for different analysis perspectives

2. **Integrate Real-Time Market Data**
   - Connect with Yahoo Finance for live stock prices and financials

3. **Personalize Recommendations**
   - Match stocks to user's risk profile using "Investor DNA"

4. **Educate While Advising**
   - Provide explanations for why a stock is recommended

5. **Simulate Risks**
   - Show worst-case scenarios before investing (Regret Prevention)

---

## SLIDE 4: Literature Survey

### Existing Solutions & Gaps

| Solution | What It Does | Gap |
|----------|--------------|-----|
| Zerodha Varsity | Education | No recommendations |
| Screener.in | Data display | Requires expertise |
| Tickertape | Analysis | Limited AI |
| Groww | Mutual funds | No stock analysis |
| ChatGPT | General AI | Not finance-specialized |

### Our Approach
Combine **Real-time Data + Multi-Agent AI + Personalization** to bridge these gaps.

---

## SLIDE 5: Proposed System

### ELIDA System Overview

**ELIDA** = Enhanced Learning Investment Decision Advisor

**Architecture Type:** Multi-Agent AI with RAG (Retrieval-Augmented Generation)

**Key Components:**
- React Frontend (User Interface)
- FastAPI Backend (Orchestration)
- 6 Specialized AI Agents
- ChromaDB Vector Store (RAG)
- SQLite Database (Persistence)

---

## SLIDE 6: System Architecture Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   User       │────▶│   React      │────▶│   FastAPI    │
│   (Browser)  │     │   Frontend   │     │   Backend    │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                     ┌────────────────────────────┼────────────────────────────┐
                     │                            ▼                            │
                     │   ┌──────────┐   ┌──────────┐   ┌──────────┐           │
                     │   │  Scout   │   │  Quant   │   │  Macro   │           │
                     │   │  Agent   │   │  Agent   │   │  Agent   │           │
                     │   └────┬─────┘   └────┬─────┘   └────┬─────┘           │
                     │        │              │              │                  │
                     │   ┌────┴─────┐   ┌────┴─────┐   ┌────┴─────┐           │
                     │   │ Philos.  │   │ Regret   │   │  Coach   │           │
                     │   │ Agent    │   │  Agent   │   │  Agent   │           │
                     │   └──────────┘   └──────────┘   └──────────┘           │
                     │                    AI AGENTS                            │
                     └─────────────────────────┬───────────────────────────────┘
                                               │
                     ┌─────────────────────────┼─────────────────────────┐
                     │                         ▼                         │
                     │   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
                     │   │ ChromaDB │   │  SQLite  │   │  Yahoo   │     │
                     │   │  (RAG)   │   │   (DB)   │   │ Finance  │     │
                     │   └──────────┘   └──────────┘   └──────────┘     │
                     │                 DATA LAYER                        │
                     └───────────────────────────────────────────────────┘
```

---

## SLIDE 7: Technology Stack

### Technologies Used

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 19, Vite, CSS | User Interface |
| **Backend** | FastAPI, Python 3.11 | API & Orchestration |
| **AI/LLM** | Google Gemini, Ollama | Intelligence |
| **Vector DB** | ChromaDB | RAG Context |
| **Database** | SQLite, SQLAlchemy | User Data |
| **Data API** | Yahoo Finance | Market Data |
| **Auth** | JWT Tokens | Security |

**Repository:** https://github.com/Pruthvi3715/VOIS-ELIDA.git

---

## SLIDE 8: AI Agents Description

### The 6 Expert Agents

| Agent | Emoji | Role | Analyzes |
|-------|-------|------|----------|
| **Scout** | 🔍 | Data Collector | Price, Volume, News, Financials |
| **Quant** | 📊 | Fundamentals | P/E, ROE, Debt, Margins |
| **Macro** | 🌍 | Market Context | VIX, Sector Trends, Economy |
| **Philosopher** | 🧠 | Quality Judge | Moat, Management, ESG |
| **Regret** | ⚠️ | Risk Simulator | Worst-case scenarios |
| **Coach** | 🎯 | Synthesizer | Final verdict & recommendation |

Each agent provides a **Score (0-100)** and **Detailed Reasoning**.

---

## SLIDE 9: Investor DNA Feature

### Personalization Engine

**User Profile Inputs:**
- Risk Tolerance (Conservative ↔ Aggressive)
- Investment Horizon (Short / Medium / Long term)
- Financial Goals (Growth, Income, Safety)
- Sectors to Avoid (Tobacco, Alcohol, Gambling)

**Stock Analysis Outputs:**
- Volatility Score
- Growth Potential
- Dividend Profile
- Sector Classification

**Result:**
- Match Score (0-100)
- Recommendation (BUY / HOLD / SELL)
- Fit Reasons & Concerns

---

## SLIDE 10: Key Features

### What ELIDA Offers

| # | Feature | Description |
|---|---------|-------------|
| 1 | 🔍 **Stock Analysis** | Multi-agent AI comprehensive analysis |
| 2 | 🧬 **Investor DNA** | Personalized profile matching |
| 3 | 📈 **Live Market** | Real-time stock prices (₹/$) |
| 4 | 💬 **AI Chatbot** | Investment Q&A assistant |
| 5 | 📜 **History** | Track past analyses |
| 6 | 💼 **Portfolio** | Manage holdings |
| 7 | 🎯 **Match Score** | 0-100 fit rating |

---

## SLIDE 11: Implementation - API Endpoints

### Backend API Structure

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/analyze/{ticker}` | GET | Full stock analysis |
| `/market-data/{ticker}` | GET | Live price data |
| `/api/v1/profile` | GET/POST | User profile |
| `/api/v1/history` | GET | Analysis history |
| `/chat/general` | POST | Chatbot queries |
| `/auth/login` | POST | Authentication |

---

## SLIDE 12: Screenshots

### Dashboard
[Insert Dashboard Screenshot - showing Live Market, Search, Recent Analyses]

### Analysis Results
[Insert Analysis Screenshot - showing Match Score, Agent Insights, Coach Verdict]

### Investor Profile
[Insert Profile Screenshot - showing Risk, Horizon, Goals settings]

### Chatbot
[Insert Chatbot Screenshot - showing conversation interface]

---

## SLIDE 13: Testing & Results

### Testing Summary

| Test Type | Tests | Pass Rate |
|-----------|-------|-----------|
| Unit Tests | 15 | 100% |
| API Tests | 8 | 100% |
| Integration | 5 | 100% |
| UAT | 5 users | Positive |

### Performance Metrics
- Analysis Time: ~30-60 seconds
- API Response: <500ms
- Market Data: Real-time updates

---

## SLIDE 14: Challenges & Solutions

### Challenges Faced

| Challenge | Solution |
|-----------|----------|
| LLM Rate Limits | Caching + Fallback to Ollama |
| Currency Symbol (₹) | Unicode escape sequences |
| Data Accuracy | Multiple source validation |
| Agent Coordination | Orchestrator design pattern |
| UI Responsiveness | React hooks & state management |

---

## SLIDE 15: Future Scope

### Roadmap

**Phase 2 (Short-term):**
- 📱 Mobile App (React Native)
- 📊 Advanced Charts (TradingView)
- 🔔 Price Alerts & Notifications
- 🤝 Social Sharing

**Phase 3 (Long-term):**
- 🧠 ML Price Prediction
- 📰 News Sentiment Analysis
- 🌐 Multi-language Support
- 💹 Mutual Fund Analysis

---

## SLIDE 16: Conclusion

### Summary

**ELIDA** successfully demonstrates:

✅ Multi-Agent AI for investment analysis
✅ Real-time market data integration
✅ Personalized "Investor DNA" matching
✅ Educational insights for learning
✅ Risk simulation before investing

### Impact
Democratizing investment advice - making professional-grade analysis accessible to retail investors.

### Learning Outcomes
- Full-stack development (React + FastAPI)
- LLM integration & prompt engineering
- RAG implementation
- Financial domain expertise

---

## SLIDE 17: References

1. Yahoo Finance API - https://pypi.org/project/yahooquery/
2. FastAPI Documentation - https://fastapi.tiangolo.com/
3. React Documentation - https://react.dev/
4. ChromaDB - https://docs.trychroma.com/
5. Google Gemini API - https://ai.google.dev/
6. NSE India - https://www.nseindia.com/
7. Zerodha Varsity - https://zerodha.com/varsity/
8. RAG Paper - Lewis et al. (2020)

---

## SLIDE 18: Thank You

### Questions?

**Team 83**

| Name | Role |
|------|------|
| Pruthviraj Shinde | Backend, AI Agents |
| Kinjal Jadhav | Frontend, UI/UX |
| Siddanth Lokhnade | Database, Documentation |

**Mentor:** Deepneel Majumdar

**GitHub:** https://github.com/Pruthvi3715/VOIS-ELIDA.git

---

**Maharashtra Institute of Management, Information Technology (MMIT)**
Loni Kalbhor, Pune, India

---
