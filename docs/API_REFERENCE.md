# API Reference

Base URL: `http://localhost:8000`

## 📊 Analysis Endpoints

### 1. One-Shot Analysis
**GET** `/analyze/{asset_id}`

Triggers the full pipeline: Ingestion -> RAG -> Agent Analysis -> Match Score.

**Parameters:**
- `asset_id` (path): Ticker symbol (e.g., `TCS.NS`, `AAPL`).
- `user_id` (query, optional): ID of the investor profile (default: `default`).

**Response:**
```json
{
  "orchestration_id": "orch_v2_match",
  "match_score": 75,
  "match_result": {
    "recommendation": "Buy",
    "breakdown": { ... }
  },
  "results": {
    "quant": { ... },
    "macro": { ... },
    "philosopher": { ... }
  }
}
```

### 2. General Research
**POST** `/chat/general`

For concept questions (e.g., "What is P/E ratio?"). Uses Wikipedia/Internet.

**Payload:**
```json
{
  "query": "What is systemic risk?"
}
```

**Response:**
```json
{
  "query": "What is systemic risk?",
  "response": "**Systemic risk** is...",
  "source": "wikipedia"
}
```

---

## 👤 Profile Endpoints

### 3. Get Profile
**GET** `/api/v1/profile/{user_id}`

Returns the Investor DNA settings.

### 4. Create/Update Profile
**POST** `/api/v1/profile`

**Payload:**
```json
{
  "user_id": "default_user",
  "risk_tolerance": "moderate",
  "custom_rules": [
    "Avoid airline stocks",
    "Focus on tech"
  ],
  "investment_style": "value"
}
```

---

## ⚙️ Utility

### 5. Health Check
**GET** `/health`

Returns `{"status": "healthy"}`.

### 6. RAG Stats
**GET** `/api/v1/rag/stats`

Returns count of documents in vector store.
