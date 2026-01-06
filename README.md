# 🎯 ELIDA - AI Investment Decision Advisor

> **Enhanced Learning Investment Decision Advisor** - Multi-Agent AI system for personalized stock analysis

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview

ELIDA is an AI-powered investment decision support system that uses **6 specialized AI agents** to analyze stocks and provide personalized recommendations based on your **Investor DNA** profile.

### 🎥 Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Agent AI** | 6 specialized agents for comprehensive analysis |
| 🧬 **Investor DNA** | Personalized recommendations based on your risk profile |
| 📊 **Real-Time Data** | Live stock prices from Yahoo Finance |
| 💬 **AI Chatbot** | Investment Q&A assistant |
| 📈 **Match Score** | 0-100 compatibility rating |
| 📜 **History** | Track all past analyses |

---

## 🏗️ Architecture

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│  React UI      │────▶│  FastAPI       │────▶│  AI Agents     │
│  (Frontend)    │     │  (Backend)     │     │  (6 Agents)    │
└────────────────┘     └────────────────┘     └────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ChromaDB        SQLite          Yahoo Finance
        (RAG)          (Users)         (Market Data)
```

### 🤖 The 6 AI Agents

| Agent | Role | Purpose |
|-------|------|---------|
| 🔍 **Scout** | Data Collector | Fetches live market data |
| 📊 **Quant** | Fundamentals | P/E, ROE, Debt analysis |
| 🌍 **Macro** | Market Context | VIX, sector trends |
| 🧠 **Philosopher** | Quality Judge | Moat, ESG, management |
| ⚠️ **Regret** | Risk Simulator | Worst-case scenarios |
| 🎯 **Coach** | Synthesizer | Final BUY/HOLD/SELL |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama (for local LLM)

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 💻 Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19, Vite, CSS |
| **Backend** | FastAPI, Python 3.11 |
| **AI/LLM** | Ollama, Groq, Gemini |
| **Vector DB** | ChromaDB |
| **Database** | SQLite + SQLAlchemy |
| **Auth** | JWT Tokens |

---

## 📁 Project Structure

```
ELIDA/
├── backend/
│   ├── app/
│   │   ├── agents/       # AI Agents (Scout, Quant, Macro, etc.)
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # RAG, Match Score services
│   │   └── main.py       # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── pages/        # Dashboard, Analysis, Profile
│   └── package.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROJECT_REPORT.md
│   ├── PPT_CONTENT.md
│   └── PRESENTATION_GUIDE.md
└── README.md
```

---

## 👥 Team

**Team 83** - Maharashtra Institute of Management, Information Technology (MMIT), Pune

| Name | Role |
|------|------|
| Pruthviraj Shinde | Backend, AI Agents |
| Kinjal Jadhav | Frontend, UI/UX |
| Siddanth Lokhnade | Database, Documentation |

**Mentor:** Deepneel Majumdar

---

## 📄 License

This project is for educational purposes as part of the MCA curriculum at MMIT, Pune.

---

## 🙏 Acknowledgments

- Yahoo Finance for market data
- Ollama for local LLM support
- ChromaDB for vector storage
- FastAPI & React communities

---

*Built with ❤️ by Team 83*
