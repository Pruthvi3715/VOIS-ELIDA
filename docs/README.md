# ELIDA | AI Financial Assistant

**ELIDA** is an advanced AI-powered agentic system designed to provide institutional-grade financial analysis to retail investors. It leverages a Multi-Agent Architecture and RAG (Retrieval-Augmented Generation) to deliver personalized, data-driven investment insights.

## 🚀 Key Features

- **Multi-Agent Intelligence**: 
  - **Scout Agent**: Fetches real-time market data (Yahoo Finance).
  - **Quant Agent**: Analyzes fundamentals (P/E, Margins, Growth).
  - **Macro Agent**: Assesses economic environment (VIX, Rates).
  - **Philosopher Agent**: Checks ethical alignment (Sin stocks, ESG).
  - **Coach Agent**: Synthesizes all insights into a final verdict.

- **Personalized "Investor DNA"**:
  - Define your Risk Tolerance, Horizon, and Ethical Filters.
  - **Custom Rules**: Add specific constraints like "Avoid airline stocks".

- **Smart Routing**:
  - Distinguishes between Stock Analysis ("TCS.NS") and General Queries ("What is P/E Ratio?").

- **Dual Interface**:
  - **Streamlit**: Data-centric dashboard for deep analysis.
  - **React**: Modern chat interface for seamless interaction.

## 🛠 Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI/LLM**: Google Gemini 1.5/2.0
- **Database**: ChromaDB (Vector Store), In-Memory (Session)
- **Frontend**: React (Vite), Streamlit
- **Data Sources**: Yahoo Finance (`yfinance`), Wikipedia

## 📦 quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd VOIS
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Set up .env with GEMINI_API_KEY
   python -m uvicorn app.main:app --reload
   ```

3. **Frontend Setup (React)**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Streamlit Setup**
   ```bash
   cd ..
   streamlit run streamlit_app.py
   ```

## 📚 Documentation

- [Architecture Guide](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
