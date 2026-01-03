# System Architecture

## High-Level Architecture
The VOIS-ELIDA system follows a modern client-server architecture with a React frontend and a FastAPI backend, powered by a Multi-Agent System (MAS).

```mermaid
graph TD
    User[User] -->|Interact| Frontend[React Frontend]
    Frontend -->|API Requests| Backend[FastAPI Backend]
    
    subgraph "Backend Core"
        Backend --> Orchestrator[Agent Orchestrator]
        Orchestrator --> Agents[AI Agents]
        Backend --> Services[Core Services]
    end
    
    subgraph "Data Layer"
        Services --> DB[(Database / Cache)]
        Services --> RAG[RAG Knowledge Base]
    end
    
    subgraph "External World"
        Services --> APIs[External Financial APIs]
        APIs -.->|Market Data| DB
    end
```

## Agent System Workflow
The core interaction is managed by the `Orchestrator`, which coordinates specialized agents to analyze financial data from different perspectives.

```mermaid
sequenceDiagram
    participant User
    participant Orch as Orchestrator
    participant Scout as Scout Agent
    participant Analysts as Analytic Agents
    participant Coach as Coach Agent
    
    User->>Orch: Request Analysis (Ticker)
    Orch->>Scout: Gather Real-time Data
    Scout-->>Orch: Market Data & News
    
    par Parallel Analysis
        Orch->>Analysts: Analyze(Data)
        Note right of Analysts: Quant, Macro, Philosopher, Regret
    end
    
    Analysts-->>Orch: Individual Scores & Insights
    
    Orch->>Coach: Synthesize & Recommend
    Coach-->>Orch: Final Recommendation (Buy/Sell/Hold)
    
    Orch->>User: Comprehensive Report
```

## Detailed Component Architecture

### Backend Components
The backend is structured into distinct layers for modularity and scalability.

```mermaid
classDiagram
    class Orchestrator {
        +run_analysis(ticker)
        +aggregate_scores()
    }
    
    class Agents {
        <<Interface>>
        +analyze(context)
    }
    class QuantAgent
    class MacroAgent
    class PhilosopherAgent
    class RegretAgent
    class CoachAgent
    class ScoutAgent
    
    Orchestrator --> Agents
    Agents <|-- QuantAgent
    Agents <|-- MacroAgent
    Agents <|-- PhilosopherAgent
    Agents <|-- RegretAgent
    Agents <|-- CoachAgent
    Agents <|-- ScoutAgent
    
    class Services {
        +market_data()
        +vector_search()
        +calculate_score()
    }
    class MarketDataService
    class RAGService
    class PortfolioService
    class MatchScoreService
    
    Agents --> Services
    Services <|-- MarketDataService
    Services <|-- RAGService
    Services <|-- PortfolioService
    Services <|-- MatchScoreService
```

### Data Providers & Services
- **CoingeckoService**: Crypto market data.
- **FredService**: Federal Reserve Economic Data.
- **RbiService**: Reserve Bank of India data.
- **RAGService**: Retrieval-Augmented Generation for context.
- **CacheService**: Performance optimization.
