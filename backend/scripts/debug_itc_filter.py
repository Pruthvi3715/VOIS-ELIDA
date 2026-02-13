"""Debug ITC ethical filter check - Full Flow"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.services.profile_service import profile_service
from app.services.match_score_service import match_score_service
from app.agents.scout import scout_agent

# 1. Get User Profile (User ID 1)
print("\n1. Fetching User Profile...")
db = SessionLocal()
dna = profile_service.get_investor_dna(db, "1")
db.close()
print(f"  Got DNA for User 1: exclude_tobacco={dna.exclude_tobacco}")

# 2. Get Asset Data
print("\n2. Fetching Asset Data for ITC.NS...")
data = scout_agent.collect_data('ITC.NS')
financials = data.get('financials', {})
print(f"  Sector: {financials.get('sector')}")
print(f"  Industry: {financials.get('industry')}")

# 3. Calculate Match Score
print("\n3. Calculating Match Score...")
# Mock agent results
agent_results = {
    "quant": {"score": 75},
    "macro": {"trend": "Neutral"},
    "philosopher": {"alignment": "Medium"},
    "regret": {"risk_level": "Medium"}
}

result = match_score_service.calculate_match_score(
    agent_results=agent_results,
    asset_data=data,
    investor_dna=dna
)

print(f"\n4. Final Result:")
print(f"  Score: {result.match_score}")
print(f"  Recommendation: {result.recommendation}")
print(f"  Ethical Penalty Applied: {result.match_score < 50}")

