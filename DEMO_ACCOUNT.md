# Demo Account Guide

## Quick Access

**Demo Login Credentials:**
- **Username**: `demo`
- **Password**: `demo123`

---

## Login Methods

### Method 1: One-Click Demo Login (Recommended)
1. Go to http://localhost:5173
2. Click the **"Try Demo Account"** button
3. Automatically logged in! ✅

### Method 2: Manual Login
1. Go to http://localhost:5173
2. Enter credentials:
   - Username: `demo`
   - Password: `demo123`
3. Click "Sign In"

---

## Demo User Profile

The demo account comes pre-configured with:

- **User ID**: 7
- **Email**: demo@elida.app
- **Risk Tolerance**: Moderate
- **Time Horizon**: 5 years
- **Investment Goals**: Growth, Income
- **Preferred Sectors**: Technology, Healthcare, Finance

This profile influences the match score algorithm to provide personalized stock recommendations.

---

## Why Authentication Might Fail

Common issues and solutions:

### 1. Backend Not Running
**Error**: Login button spins forever or shows "Login failed"

**Fix**:
```bash
cd backend
python -m uvicorn app.main:app --reload
```
Verify: http://localhost:8000/health should return `{"status":"ok"}`

### 2. Database Not Initialized
**Error**: "User not found" or database errors

**Fix**:
```bash
cd backend
python setup_demo_account.py
```

### 3. Wrong Password
**Error**: "Invalid username or password"

**Fix**:
```bash
cd backend
python fix_demo_password.py
```

### 4. Token Expired
**Error**: Authentication errors after being logged in

**Fix**: Just log out and log back in (tokens expire after 24 hours)

---

## For Hackathon Judges

**Make it easy for judges:**

1. **Add a note on your presentation**:
   ```
   Demo Login: demo / demo123
   Or click "Try Demo Account" button
   ```

2. **Keep the demo account working**:
   - Test before the presentation
   - Have `setup_demo_account.py` ready to re-run if needed

3. **Backup: Skip Auth Entirely** (Emergency Only):
   - The app already supports `user_id="default"` for unauthenticated access
   - Analysis works without login, but profile features require auth

---

## Testing the Demo Account

### Quick Test Script:
```bash
cd backend
python -c "
import requests

# Test login
response = requests.post(
    'http://localhost:8000/api/auth/login',
    json={'username': 'demo', 'password': 'demo123'}
)

if response.status_code == 200:
    data = response.json()
    print(f'✅ Demo login working!')
    print(f'User ID: {data[\"user_id\"]}')
    print(f'Token: {data[\"access_token\"][:30]}...')
else:
    print(f'❌ Login failed: {response.text}')
"
```

---

## Troubleshooting Checklist

Before your demo:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can access login page
- [ ] "Try Demo Account" button visible
- [ ] Demo login works (click button → redirects to dashboard)
- [ ] Can analyze stocks (try AAPL or RELIANCE.NS)

---

## Re-creating Demo Account

If something goes wrong, you can always recreate:

```bash
cd backend

# Delete existing demo user
python -c "
from app.database import SessionLocal
from app.models.db_models import User
db = SessionLocal()
demo = db.query(User).filter(User.username == 'demo').first()
if demo:
    db.delete(demo)
    db.commit()
    print('Demo user deleted')
db.close()
"

# Create fresh demo account
python setup_demo_account.py
```

---

## Security Note

**This is a DEMO account for hackathon/testing only.**

For production:
- Change the password
- Add rate limiting
- Implement proper session management
- Add CAPTCHA protection
- Use environment variables for secrets

---

## Support

If demo login still fails after trying all fixes:

1. Check backend logs for errors
2. Check browser console (F12) for frontend errors
3. Verify database file exists: `backend/elida.db`
4. Try restarting both backend and frontend

**Last resort**: Use the app without authentication - analysis still works with default profile.
