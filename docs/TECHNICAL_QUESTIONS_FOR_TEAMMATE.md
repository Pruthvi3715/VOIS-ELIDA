# 🎯 Technical Questions for YOU (Non-Presenter Teammate)

> **As a team member who is NOT presenting, you should be prepared for these questions that judges/audience might direct specifically to you to test your understanding of the project.**

---

## ⚠️ WHY YOU'LL BE ASKED QUESTIONS

Judges often ask non-presenters to:
1. **Test team dynamics** - Ensure everyone contributed
2. **Verify understanding** - Not just memorized content
3. **Check depth of knowledge** - Beyond slides
4. **Assess collaborative work** - Who did what

---

## 🔥 HIGH PROBABILITY QUESTIONS (Prepare These First!)

### Your Specific Contributions
1. **"What was YOUR specific contribution to this project?"**
   - Be specific: "I implemented the Quant Agent" not "I helped with backend"
   
2. **"Which agent did you develop? Explain how it works."**

3. **"Walk me through a piece of code you wrote."**

4. **"What was the most challenging bug you fixed?"**

5. **"How did you coordinate with your teammates?"**

---

## 🧠 Understanding the Core Concept

### Multi-Agent Architecture
6. **Why 6 agents? Why not 3 or 10?**
   - Answer: Each agent has a specialized role mirroring real investment analysis teams
   
7. **What's the difference between Scout and other agents?**
   - Answer: Scout collects data; others analyze it

8. **Can you explain what happens step-by-step when I enter "TCS" to analyze?**

9. **Why call it "Orchestrator"? What does it orchestrate?**

### Behavioral Finance
10. **What is Prospect Theory in simple terms?**
    - Answer: People feel losses more strongly than gains (loss aversion)

11. **How does the Regret Agent work differently from other agents?**

12. **What does "Investor DNA" mean?**

---

## 💻 Technical Questions YOU Must Know

### Backend Basics
13. **What framework is used for backend? Why?**
    - FastAPI - async support, auto-documentation, fast performance

14. **What database are you using? Why SQLite?**
    - SQLite - lightweight, no setup, suitable for prototype/demo

15. **What is ChromaDB used for?**
    - Vector storage for RAG (Retrieval Augmented Generation)

16. **What does RAG mean and why is it important?**
    - Retrieval Augmented Generation - grounds LLM responses in factual data

### Frontend Basics
17. **What frontend framework is used?**
    - React 19 with Vite

18. **How does the frontend communicate with backend?**
    - REST API calls using fetch/axios

19. **Where is the auth token stored?**
    - localStorage or context

### LLM Strategy
20. **What LLMs does the system support?**
    - Ollama (local), Groq (cloud), Gemini (cloud)

21. **What happens if Ollama is not running?**
    - Fallback to Groq → then Gemini

22. **Why use local LLM (Ollama)?**
    - Privacy, no API costs, works offline

---

## 📊 Data & Analysis Questions

23. **Where does stock data come from?**
    - Yahoo Finance API, with Screener.in fallback for Indian stocks

24. **What financial metrics does the system analyze?**
    - P/E, ROE, Debt/Equity, Revenue Growth, etc.

25. **How is the Match Score (0-100) calculated?**
    - Based on Investor DNA matching with stock characteristics

26. **What does BUY/HOLD/SELL depend on?**
    - Match score + all agent recommendations + investor profile

---

## 🔐 Security Questions

27. **How is user authentication handled?**
    - JWT tokens

28. **How are passwords stored?**
    - Hashed (not plain text)

29. **How are API keys protected?**
    - Environment variables (.env file)

---

## 🚫 Questions to AVOID Saying "I Don't Know"

### Redirect Strategies:
- "That specific implementation was handled by [teammate], but I can explain the general approach..."
- "From what I understand of that module..."
- "We collaborated on this - here's how it works..."

---

## 📝 QUICK REFERENCE ANSWERS

| Question | Quick Answer |
|----------|--------------|
| Tech stack? | React + FastAPI + SQLite + ChromaDB |
| Why multi-agent? | Specialized analysis like real investment teams |
| What's unique? | Behavioral finance + LLM + Investor DNA matching |
| How fast? | < 5 seconds per analysis |
| Target users? | Retail investors with limited financial literacy |
| LLM? | Ollama/Groq/Gemini with fallback chain |
| Data source? | Yahoo Finance + Screener.in |
| Auth? | JWT tokens |
| Why this project? | 73% Indians are financially illiterate |

---

## 🎓 Questions You MUST Be Ready For

### "Explain this to me like I'm not technical"
Practice explaining:
1. **Multi-Agent System**: "Like having 6 experts - analyst, economist, psychologist, risk manager - all reviewing your investment together"
2. **Investor DNA**: "Like a compatibility test between you and a stock"
3. **Behavioral Finance**: "Understanding why people make emotional money decisions and helping them avoid it"
4. **RAG**: "The AI fact-checks itself using real financial data"

### "What would you do differently?"
Have 2-3 honest improvements ready:
- Better testing coverage
- Real-time stock price updates
- Mobile app version
- More extensive user testing

### "What did you learn?"
Technical: Working with LLMs, multi-agent systems, RAG
Non-technical: Team collaboration, project management, time constraints

---

## 🎯 ROLE-SPECIFIC PREPARATION

### If you worked on Backend (Pruthviraj):
- Be ready to explain agent code flow
- Know the orchestrator logic
- Understand LLM integration

### If you worked on Frontend (Kinjal):
- Explain component structure
- Auth flow on frontend
- State management

### If you worked on Database/Docs (Siddanth):
- Database schema
- API documentation
- Testing approach

---

## ⚡ LAST-MINUTE TIPS

1. **Don't contradict your presenter** - If unsure, support their answer
2. **Use diagrams in your head** - Visualize the architecture when explaining
3. **Be honest about limitations** - "We're working on that" is okay
4. **Show enthusiasm** - Judges notice passion
5. **Mention specific numbers** - "6 agents", "< 5 seconds", "99.5% uptime"

---

> **Remember: Judges want to see teamwork, understanding, and genuine knowledge - not perfect answers!**

---

*Prepared for ELIDA Team 83 - VOIS Innovation Marathon 2026*
