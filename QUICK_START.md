# ELIDA - Quick Start Guide

## The Problem You Just Had

**Error**: "Analysis failed. Please try again."

**Root Cause**: Backend server was not running

---

## How to Start the Application

### Method 1: Using Batch Files (Easiest)

1. **Start Backend** (in one terminal):
   - Double-click `START_BACKEND.bat`
   - Wait until you see: "Application startup complete"
   - Keep this window open

2. **Start Frontend** (in another terminal):
   - Double-click `START_FRONTEND.bat`
   - Wait until you see: "Local: http://localhost:5173"
   - Keep this window open

3. **Open Browser**:
   - Go to: http://localhost:5173

---

### Method 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## Troubleshooting

### "Analysis failed. Please try again."

**Possible Causes:**

1. **Backend not running** ✅ MOST COMMON
   - Solution: Start backend with `START_BACKEND.bat`
   - Verify: Open http://localhost:8000/docs (should show API docs)

2. **Wrong API URL in frontend**
   - Check: `frontend/src/api.js` should have `http://localhost:8000`

3. **CORS error**
   - Check browser console (F12) for CORS errors
   - Backend should allow `http://localhost:5173`

4. **Groq API rate limit**
   - Wait 1 minute and try again
   - Check backend logs for "rate limit" messages

5. **Invalid stock ticker**
   - Use format: `AAPL` for US stocks, `RELIANCE.NS` for Indian stocks

---

## Testing the Backend Directly

To verify backend is working without the frontend:

```bash
cd backend
python TEST_FULL_ANALYSIS.py "AAPL"
```

If this works but frontend doesn't, the issue is in frontend-backend communication.

---

## Quick Health Check

**Is Backend Running?**
```bash
curl http://localhost:8000/api/v1/health
```
Should return: `{"status":"healthy"}`

**Is Frontend Running?**
```bash
curl http://localhost:5173
```
Should return HTML content

---

## For Hackathon Demo

**Pre-Demo Checklist:**

- [ ] Backend running (`START_BACKEND.bat`)
- [ ] Frontend running (`START_FRONTEND.bat`)
- [ ] Test with AAPL (should work in ~20 seconds)
- [ ] Test with RELIANCE.NS (should work in ~20 seconds)
- [ ] Browser on http://localhost:5173
- [ ] Backend logs visible (for debugging if needed)

**Demo Stocks:**
- ✅ AAPL - Match Score ~56, Hold
- ✅ RELIANCE.NS - Match Score ~51, Hold
- ✅ TSLA - Match Score ~25, Avoid (good for showing low scores)
- ⚠️ Avoid: Very small/obscure stocks (may fail data fetch)

---

## Error Recovery

**If frontend shows errors:**
1. Check backend logs for actual error
2. Try re-analyzing (click "Re-analyze" button)
3. Try a different stock (like AAPL)
4. Restart backend if needed

**If backend crashes:**
1. Check backend terminal for error message
2. Restart with `START_BACKEND.bat`
3. Common causes:
   - Groq API key expired/invalid
   - Database locked
   - Port 8000 already in use

---

## Contact During Hackathon

If something breaks during the hackathon:

1. **Check backend logs first** - 90% of errors are there
2. **Try TEST_FULL_ANALYSIS.py** - Isolates backend issues
3. **Check browser console (F12)** - Shows frontend errors
4. **Restart both servers** - Nuclear option that usually works

---

Good luck with your presentation! 🚀
