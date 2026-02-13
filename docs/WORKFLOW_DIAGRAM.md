# ELIDA — Workflow Diagrams

> User workflows, agent internal processes, and DevOps pipelines

---

## 1. User Workflow — Stock Analysis

```mermaid
flowchart TD
    Start(["👤 User Opens App"]) --> Login{"Logged In?"}
    Login -->|No| Auth["Login / Register"]
    Auth --> SetDNA["Set Investor DNA Profile"]
    SetDNA --> Dashboard
    Login -->|Yes| Dashboard["📊 Dashboard"]

    Dashboard --> Search["🔍 Search Stock\n(name or ticker)"]
    Search --> Resolve["Auto-resolve Ticker\nApple → AAPL\nMRF → MRF.NS"]
    Resolve --> Analyze["▶️ Run Analysis"]

    Analyze --> Loading["⏳ Loading Screen\nAgent-by-agent progress"]
    Loading --> Results["📋 Analysis Results Page"]

    Results --> View_Agents["View Agent Cards\nQuant | Macro | Philosopher | Regret"]
    Results --> View_Match["View Match Score\nRadial gauge + breakdown"]
    Results --> View_Coach["View Coach Verdict\nFinal recommendation"]
    Results --> View_Chart["View Price Chart\nHistorical data"]

    View_Agents --> DeepDive["🔎 Agent Deep Dive\nDetailed analysis text"]
    View_Match --> DNA_Edit["✏️ Edit Investor DNA\nRecalculate match"]

    Results --> Compare["⚔️ Compare with\nanother stock"]
    Results --> Save["💾 Saved to History\nautomatically"]

    Compare --> CompareView["Side-by-side\nagent comparison"]
    Save --> History["📜 History Page\nAll past analyses"]

    History --> Revisit["Re-view any\npast analysis"]

    Dashboard --> Portfolio["📁 Portfolio Scanner"]
    Portfolio --> MultiAdd["Add multiple tickers"]
    MultiAdd --> BatchAnalysis["Batch analysis\n(background)"]
    BatchAnalysis --> PortfolioView["Portfolio overview\nwith match scores"]

    style Start fill:#667eea,color:#fff
    style Results fill:#48bb78,color:#fff
    style Loading fill:#ed8936,color:#fff
    style CompareView fill:#4fd1c5,color:#fff
```

---

## 2. Agent Internal Workflow

```mermaid
flowchart TD
    subgraph Each_Agent["Each Agent (Quant / Macro / Philosopher / Regret)"]
        direction TB
        A["Receive Context\nfrom Orchestrator"] --> B["calculate_data_quality()\nAssess input completeness"]
        B --> C["Build Prompt\nwith JSON output format"]
        C --> D["call_llm()\nOpenRouter → Groq → Ollama → Gemini"]
        D --> E{"LLM Response OK?"}
        E -->|Yes| F["_parse_response()\nExtract JSON from text"]
        E -->|No| G["Sector-based Fallback\nRule-based defaults"]
        G --> F
        F --> H{"JSON Valid?"}
        H -->|Yes| I["Validate Fields\nalignment ∈ [Low/Medium/High]\nrisk_level ∈ [Low/Medium/High]"]
        H -->|No| J["Regex Fallback Extraction\nextract_level(), extract_confidence()"]
        J --> I
        I --> K["Derive Numeric Score\nCategory → Score map\n+ confidence adjustment"]
        K --> L["format_output()\n{score, output, confidence,\ndata_quality, analysis}"]
    end

    style A fill:#667eea,color:#fff
    style D fill:#ed8936,color:#fff
    style G fill:#fc8181,color:#fff
    style L fill:#48bb78,color:#fff
```

---

## 3. Score Derivation Workflow

```mermaid
flowchart LR
    subgraph Quant["📊 Quant Agent"]
        Q_LLM["LLM extracts\nscore directly"] --> Q_Score["Score: 0-100"]
    end

    subgraph Macro["🌍 Macro Agent"]
        M_Cat["LLM → Trend Category"] --> M_Map["Bullish: 75\nNeutral: 50\nBearish: 30"]
        M_Map --> M_Adj["× (0.7 + 0.3 × confidence/100)"]
        M_Adj --> M_Score["Score: 0-100"]
    end

    subgraph Phil["🧠 Philosopher Agent"]
        P_Cat["LLM → Alignment"] --> P_Map["High: 80\nMedium: 55\nLow: 30"]
        P_Map --> P_Adj["× (0.7 + 0.3 × confidence/100)"]
        P_Adj --> P_Score["Score: 0-100"]
    end

    subgraph Regret["⚠️ Regret Agent"]
        R_Cat["LLM → Risk Level"] --> R_Map["Low: 80\nMedium: 55\nHigh: 30\n(inverted)"]
        R_Map --> R_Adj["× (0.7 + 0.3 × confidence/100)"]
        R_Adj --> R_Score["Score: 0-100"]
    end

    subgraph Match["📊 Match Score Service"]
        Q_Score --> Weighted
        M_Score --> Weighted
        P_Score --> Weighted
        R_Score --> Weighted
        DNA["DNA Match\n(risk + style + ethics)"] --> Weighted
        Weighted["Weighted Sum\nQ×35% + M×10%\nP×10% + R×20%\nDNA×25%"] --> Final["Match Score\n0-100%"]
    end

    Final --> Rec{"Recommendation"}
    Rec -->|"≥75"| Buy["✅ Strong Buy"]
    Rec -->|"65-74"| MildBuy["📈 Buy"]
    Rec -->|"45-64"| Hold["⏸️ Hold"]
    Rec -->|"30-44"| MildSell["📉 Sell"]
    Rec -->|"<30"| Sell["❌ Strong Sell"]

    style Final fill:#667eea,color:#fff
    style Buy fill:#48bb78,color:#fff
    style Sell fill:#e53e3e,color:#fff
```

---

## 4. Orchestrator Pipeline Workflow

```mermaid
flowchart TD
    A["📥 API receives\nanalyze_asset(ticker)"] --> B["Step 1: Resolve Ticker\nMRF → MRF.NS"]
    B --> C["Step 2: Ingest Asset\nClear old cache"]
    C --> D["Scout collects data\nYahoo + FRED + RBI"]
    D --> E["Store in ChromaDB\n(RAG memory)"]
    E --> F["Step 3: Retrieve Context\n15 asset docs + 3 macro docs"]
    F --> G["Inject: Company ID\n+ Cached data\n+ Investor DNA rules"]
    G --> H["Step 4: Parallel Agent Execution\n4 agents via ThreadPoolExecutor"]

    H --> I["Quant: 35"]
    H --> J["Macro: 45"]
    H --> K["Philosopher: 45"]
    H --> L["Regret: 27"]

    I & J & K & L --> M["Step 5: Calculate Match Score\nWeighted + DNA matching"]
    M --> N["Step 6: Store Agent Insights\nback to RAG"]
    N --> O["Step 7: Coach Synthesis\nRetrieve insights → LLM → Verdict"]
    O --> P["Step 8: Save to History\nSQLite persistence"]
    P --> Q["📤 Return Full Response\nagent_results + match_score\n+ coach_verdict + market_data"]

    style A fill:#667eea,color:#fff
    style H fill:#ed8936,color:#fff
    style M fill:#4fd1c5,color:#fff
    style O fill:#b794f4,color:#fff
    style Q fill:#48bb78,color:#fff
```

---

## 5. DevOps & Startup Workflow

```mermaid
flowchart TD
    subgraph Setup["🔧 Initial Setup"]
        Clone["git clone"] --> InstallBE["pip install -r requirements.txt"]
        InstallBE --> InstallFE["cd frontend && npm install"]
        InstallFE --> EnvFile["Create backend/.env\nLLM_PROVIDER, API keys"]
    end

    subgraph Start["🚀 Start Servers"]
        EnvFile --> StartBE["START_BACKEND.bat\nuvicorn app.main:app\n--reload --port 8000"]
        EnvFile --> StartFE["START_FRONTEND.bat\nnpm run dev\n→ port 5173"]
    end

    subgraph Runtime["⚡ Runtime"]
        StartBE --> BE_Ready["Backend Ready\nhttp://localhost:8000"]
        StartFE --> FE_Ready["Frontend Ready\nhttp://localhost:5173"]
        BE_Ready --> API_Docs["Swagger: /docs\nOpenAPI: /api/v1/openapi.json"]
        FE_Ready --> App["Open App in Browser"]
    end

    style Setup fill:#667eea,color:#fff
    style Start fill:#ed8936,color:#fff
    style Runtime fill:#48bb78,color:#fff
```
