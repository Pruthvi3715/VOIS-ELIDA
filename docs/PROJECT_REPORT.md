# ELIDA - AI Investment Decision Advisor
## Project Report

---

**Team Number:** 83

**Team Members:**
- Pruthviraj Shinde
- Kinjal Jadhav
- Siddanth Lokhnade

**Project Mentor:** Deepneel Majumdar

**Institution:** Maharashtra Institute of Management, Information Technology (MMIT), Loni Kalbhor, Pune, India

**Semester:** 3 | **Academic Year:** 2025-26

**GitHub Repository:** https://github.com/Pruthvi3715/VOIS-ELIDA.git

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Literature Survey](#4-literature-survey)
5. [Proposed System](#5-proposed-system)
6. [System Architecture](#6-system-architecture)
7. [Technology Stack](#7-technology-stack)
8. [Module Description](#8-module-description)
9. [Implementation Details](#9-implementation-details)
10. [Screenshots](#10-screenshots)
11. [Testing](#11-testing)
12. [Future Scope](#12-future-scope)
13. [Conclusion](#13-conclusion)
14. [References](#14-references)

---

## 1. Abstract

ELIDA (Enhanced Learning Investment Decision Advisor) is an AI-powered investment decision support system designed to help retail investors make informed, data-driven investment decisions. The system utilizes a multi-agent AI architecture where specialized agents analyze stocks from different perspectives—quantitative analysis, macroeconomic context, business quality, and risk assessment—before synthesizing a personalized recommendation.

The key innovation is the "Investor DNA" matching system, which creates a personalized profile based on the user's risk tolerance, investment horizon, and financial goals, then matches stocks to this profile to provide tailored recommendations. The system integrates real-time market data from Yahoo Finance, uses Google Gemini as the primary LLM, and employs ChromaDB for RAG-based context retrieval.

**Keywords:** Artificial Intelligence, Investment Analysis, Multi-Agent Systems, RAG, LLM, Fintech

---

## 2. Introduction

### 2.1 Background

The retail investment landscape has grown significantly in recent years, especially in India where Demat accounts crossed 10 crore in 2023. However, studies show that approximately 70% of retail investors lose money in their first year of trading. This high failure rate is attributed to:

- Lack of financial literacy
- Emotional decision-making
- Information overload
- No access to professional advice

### 2.2 Motivation

Traditional investment advisory services are expensive and inaccessible to most retail investors. While information is freely available, the challenge lies in interpreting this data correctly and making decisions that align with one's personal financial situation.

ELIDA aims to democratize investment advice by providing AI-powered, personalized recommendations that consider both quantitative metrics and qualitative factors.

### 2.3 Scope

The project covers:
- Stock analysis for Indian (NSE/BSE) and US markets
- Real-time market data integration
- Multi-agent AI analysis system
- Personalized investor profiling
- Portfolio management capabilities
- Educational chatbot assistance

---

## 3. Problem Statement

**Primary Problem:** Retail investors lack access to personalized, comprehensive investment analysis that considers their individual risk profile and financial goals.

**Secondary Problems:**
1. Information overload from multiple financial data sources
2. Difficulty understanding complex financial metrics
3. Emotional bias in investment decisions
4. No systematic approach to risk assessment
5. Lack of affordable personalized advisory services

**Objective:** To develop an AI-powered investment decision support system that:
- Provides personalized stock recommendations
- Uses multiple AI agents for balanced analysis
- Integrates real-time market data
- Educates users through explanatory insights
- Simulates potential risks before investing

---

## 4. Literature Survey

### 4.1 Existing Solutions

| Solution | Type | Limitations |
|----------|------|-------------|
| Zerodha Varsity | Educational | No personalized recommendations |
| Screener.in | Data Platform | Requires financial expertise |
| Tickertape | Analysis Tool | Limited AI integration |
| Groww Advisory | Mutual Funds | No individual stock analysis |
| ChatGPT | General AI | Not specialized for finance |

### 4.2 Research Papers Referenced

1. **Multi-Agent Systems for Financial Trading** - Explores autonomous agents for market analysis
2. **RAG for Domain-Specific Applications** - Retrieval-augmented generation for accurate responses
3. **Behavioral Finance** - Understanding investor psychology and biases
4. **Robo-Advisors Evolution** - Automated investment management systems

### 4.3 Gap Analysis

Existing solutions either provide raw data (requiring expertise) or generic advice (not personalized). ELIDA bridges this gap by combining:
- Real-time data + AI interpretation + Personalization

---

## 5. Proposed System

### 5.1 System Overview

ELIDA is a web-based application with:
- **React Frontend** for user interface
- **FastAPI Backend** for orchestration
- **Multi-Agent AI System** for analysis
- **ChromaDB** for RAG knowledge base
- **SQLite** for user data persistence

### 5.2 Key Features

| Feature | Description |
|---------|-------------|
| Stock Analysis | Multi-agent AI analysis with scoring |
| Investor DNA | Personalized profile matching |
| Live Market | Real-time stock prices |
| AI Chatbot | Investment Q&A assistance |
| History | Track past analyses |
| Portfolio | Manage stock holdings |

### 5.3 Unique Selling Points

1. **Investor DNA Matching** - Personalized recommendations
2. **Multi-Agent Analysis** - Multiple expert perspectives
3. **Regret Simulation** - Pre-mortem risk assessment
4. **Educational Insights** - Learn while investing

---

## 6. System Architecture

### 6.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                  (React Frontend)                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY                              │
│                  (FastAPI Backend)                          │
├─────────────────────────────────────────────────────────────┤
│  Smart Router │ Auth (JWT) │ Orchestrator │ History API    │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ AI AGENTS    │  │ DATA LAYER   │  │ EXTERNAL     │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ Scout Agent  │  │ ChromaDB     │  │ Yahoo Finance│
│ Quant Agent  │  │ SQLite       │  │ Gemini API   │
│ Macro Agent  │  │ Cache        │  │ Ollama       │
│ Phil Agent   │  └──────────────┘  └──────────────┘
│ Regret Agent │
│ Coach Agent  │
└──────────────┘
```

### 6.2 Data Flow

1. User enters stock symbol (e.g., TCS.NS)
2. Smart Router identifies intent → Financial Analysis
3. Orchestrator triggers Scout Agent → Collect data
4. Data stored in ChromaDB for RAG retrieval
5. Sequential analysis by Quant, Macro, Phil, Regret agents
6. Each agent retrieves context from RAG
7. Coach Agent synthesizes all insights
8. Match Score calculated against Investor DNA
9. Results displayed to user + saved to history

---

## 7. Technology Stack

### 7.1 Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.0 | UI Framework |
| Vite | 7.3 | Build Tool |
| React Router | 7.0 | Navigation |
| Lucide React | - | Icons |
| CSS (Custom) | - | Styling |

### 7.2 Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11 | Language |
| FastAPI | 0.104 | API Framework |
| Uvicorn | - | ASGI Server |
| SQLAlchemy | 2.0 | ORM |
| Pydantic | 2.0 | Validation |

### 7.3 AI/ML Technologies

| Technology | Purpose |
|------------|---------|
| Google Gemini | Primary LLM |
| Ollama | Local LLM Fallback |
| ChromaDB | Vector Database (RAG) |
| Sentence Transformers | Embeddings |

### 7.4 Data Sources

| Source | Data Type |
|--------|-----------|
| Yahoo Finance (yahooquery) | Stock prices, financials |
| News APIs | Market news |

---

## 8. Module Description

### 8.1 User Authentication Module

- JWT-based authentication
- User registration and login
- Token validation middleware
- Session management

### 8.2 Investor Profile Module

- Risk tolerance assessment
- Investment horizon selection
- Financial goals configuration
- Sector preferences (avoid/prefer)
- Profile persistence in SQLite

### 8.3 Market Data Module

- Real-time price fetching
- Historical data retrieval
- Technical indicators
- Currency detection (₹ for Indian, $ for US)

### 8.4 AI Agent Module

**Scout Agent:**
- Collects financial data from Yahoo Finance
- Extracts key metrics (P/E, ROE, Debt ratios)
- Stores data in ChromaDB

**Quant Agent:**
- Analyzes fundamental metrics
- Compares to industry benchmarks
- Provides quantitative score (0-100)

**Macro Agent:**
- Evaluates market conditions
- Analyzes sector trends
- Considers VIX, interest rates

**Philosopher Agent:**
- Assesses business quality
- Evaluates competitive moat
- Checks ESG factors

**Regret Agent:**
- Simulates worst-case scenarios
- Calculates potential downside
- Provides risk warnings

**Coach Agent:**
- Synthesizes all agent insights
- Generates final recommendation
- Creates readable summary

### 8.5 Analysis History Module

- Save analysis results
- Retrieve past analyses
- Filter and search functionality
- Export capabilities

### 8.6 Chatbot Module

- General investment Q&A
- Context-aware responses
- Quick actions for analysis

---

## 9. Implementation Details

### 9.1 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze/{ticker}` | GET | Full stock analysis |
| `/market-data/{ticker}` | GET | Real-time price data |
| `/api/v1/profile` | GET/POST | User profile management |
| `/api/v1/history` | GET | Analysis history |
| `/chat/general` | POST | Chatbot queries |
| `/auth/login` | POST | User authentication |

### 9.2 Database Schema

**Users Table:**
- id, email, password_hash, created_at

**InvestorProfile Table:**
- id, user_id, risk_tolerance, investment_horizon, goals, avoid_sectors

**AnalysisHistory Table:**
- id, user_id, query, query_type, result, timestamp

### 9.3 Key Algorithms

**Match Score Calculation:**
```
match_score = weighted_average(
    quant_score × profile_weight,
    macro_score × timing_weight,
    phil_score × quality_weight,
    regret_adjustment
)
```

**RAG Retrieval:**
```
1. Embed user query using sentence-transformers
2. Search ChromaDB for similar chunks
3. Retrieve top-k relevant context
4. Inject context into LLM prompt
5. Generate response
```

---

## 10. Screenshots

### 10.1 Dashboard
[Dashboard showing Live Market, Recent Analyses, and Search bar]

### 10.2 Analysis Results
[Stock analysis with Match Score, Agent Insights, Coach Verdict]

### 10.3 Investor Profile
[Profile settings with Risk Tolerance, Goals, Preferences]

### 10.4 Chatbot
[AI Chatbot interface with conversation]

### 10.5 History Page
[Analysis history table view]

---

## 11. Testing

### 11.1 Unit Testing

| Module | Tests | Status |
|--------|-------|--------|
| Authentication | Login, Register, Token | ✓ Pass |
| Market Data | Price fetch, Currency | ✓ Pass |
| AI Agents | Score generation | ✓ Pass |
| Profile | CRUD operations | ✓ Pass |

### 11.2 Integration Testing

| Flow | Description | Status |
|------|-------------|--------|
| End-to-end Analysis | Full stock analysis flow | ✓ Pass |
| Profile + Analysis | Personalized recommendations | ✓ Pass |
| History Persistence | Save and retrieve | ✓ Pass |

### 11.3 User Acceptance Testing

- Tested with 5 beta users
- Feedback incorporated into UI improvements
- Average task completion time: 45 seconds

---

## 12. Future Scope

### 12.1 Short-term Enhancements

1. Mobile application (React Native)
2. Advanced charting (TradingView integration)
3. Price alerts and notifications
4. Social sharing of analyses

### 12.2 Long-term Roadmap

1. Machine learning price prediction models
2. Sentiment analysis from news and social media
3. Mutual fund and ETF analysis
4. Multi-language support (Hindi, Marathi)
5. Integration with trading platforms

### 12.3 Research Opportunities

1. Improving agent accuracy with fine-tuned models
2. Behavioral finance integration
3. Portfolio optimization algorithms

---

## 13. Conclusion

ELIDA successfully demonstrates the potential of multi-agent AI systems in financial technology. By combining real-time market data, multiple analytical perspectives, and personalized user profiling, the system provides accessible, understandable, and actionable investment recommendations.

**Key Achievements:**
- ✅ Functional multi-agent AI analysis system
- ✅ Real-time market data integration
- ✅ Personalized Investor DNA matching
- ✅ User-friendly React interface
- ✅ RAG-based context retrieval for accurate insights

**Impact:**
The project demonstrates how AI can democratize financial advice, making sophisticated analysis accessible to retail investors who previously lacked access to personalized guidance.

**Learning Outcomes:**
- Full-stack web development (React + FastAPI)
- LLM integration and prompt engineering
- RAG implementation with vector databases
- Financial domain knowledge

---

## 14. References

1. Yahoo Finance API Documentation - https://pypi.org/project/yahooquery/
2. FastAPI Documentation - https://fastapi.tiangolo.com/
3. React Documentation - https://react.dev/
4. ChromaDB Documentation - https://docs.trychroma.com/
5. Google Gemini API - https://ai.google.dev/
6. "Multi-Agent Systems" - Wooldridge, M. (2009)
7. "Retrieval-Augmented Generation" - Lewis et al. (2020)
8. NSE India - https://www.nseindia.com/
9. Zerodha Varsity - https://zerodha.com/varsity/

---

## Appendix A: Installation Guide

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
```
GEMINI_API_KEY=your_api_key
LLM_PROVIDER=gemini
```

---

## Appendix B: Team Contributions

| Member | Contributions |
|--------|---------------|
| Pruthviraj Shinde | Backend, AI Agents, Architecture |
| Kinjal Jadhav | Frontend, UI/UX, Testing |
| Siddanth Lokhnade | Database, Documentation, Research |

---

*Report prepared by Team 83*
*Maharashtra Institute of Management, Information Technology (MMIT)*
*Loni Kalbhor, Pune, India*
