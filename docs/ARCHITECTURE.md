# Architecture Guide

## 🏗 System Overview

ELIDA relies on a **Hub-and-Spoke** architecture where a central **Orchestrator** manages data flow between the User, Data Sources, the RAG Knowledge Base, and specialized AI Agents.

## 🔄 Data Flow Diagram

```mermaid
graph TD
    User[User] -->|Query| API[FastAPI Backend]
    API -->|Intent| Router{Smart Router}
    
    %% Branch 1: General Knowledge
    Router -->|General Question| Research[General Chat Service]
    Research -->|Search| Wiki[Wikipedia/Google]
    Research -->|Response| User
    
    %% Branch 2: Financial Analysis
    Router -->|Stock Ticker| Orch[Financial Orchestrator]
    
    Orch -->|1. Ingest| Scout[Scout Agent]
    Scout -->|Fetch| Yahoo[Yahoo Finance]
    Scout -->|Store| RAG[(ChromaDB / Vector Store)]
    
    Orch -->|2. Retrieve Context| RAG
    
    Orch -->|3. Analyze| Agents
    subgraph "Agent Swarm"
        Quant[Quant Agent] -->|Fundamentals| RAG
        Macro[Macro Agent] -->|Trends| RAG
        Phil[Philosopher Agent] -->|Ethics| RAG
        Regret[Regret Agent] -->|Risk| RAG
    end
    
    Orch -->|4. Calculate Score| MatchService[Match Score Service]
    MatchService -->|Profile| UserDNA[Investor DNA]
    
    Orch -->|5. Synthesize| Coach[Coach Agent]
    Coach -->|Verdict| User
```

## 🤖 The Agents

Each agent has a specific persona and specialized prompt:

| Agent | Role | Tools/Data |
|-------|------|------------|
| **Scout** | Data Ingestion | YahooQuery, yfinance. Fetches Price, P/E, News. |
| **Quant** | Fundamental Analysis | Analyzes Balance Sheets, Profitability, Valuation. |
| **Macro** | Market Context | Analyzes VIX, Bond Yields, Inflation Trends. |
| **Philosopher** | Ethical Alignment | Checks against User's "Sin Stock" filters. |
| **Regret** | Risk Simulation | Simulates worst-case scenarios (Pre-Mortem). |
| **Coach** | Synthesis | Combines all insights into a final recommendation. |

## 🧬 smart Routing

The system uses Regex and Keyword matching to classify intent:
1.  **Ticker Pattern** (e.g., "TCS.NS", "AAPL"): Trigger full Financial Analysis.
2.  **General Text** (e.g., "What is EBITDA?"): Trigger General Research (Lightweight RAG).

## 💾 RAG Implementation
- **Vector Store**: ChromaDB (Transient/Persistent).
- **Embedding**: `sentence-transformers/all-MiniLM-L6-v2`.
- **Strategy**: 
    - **Step 1**: Ingest Asset Data (Financials, News) -> Chunk -> Embed.
    - **Step 2**: Agents query specifically for their domain (e.g., Quant asks for "financial ratios").
    - **Step 3**: Agents write their *Insights* back to RAG.
    - **Step 4**: Coach queries for "Agent Insights" to synthesize.
