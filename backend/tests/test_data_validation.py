"""
Test data validation and anomaly detection for ITC.NS
"""
import json
import sys
sys.path.insert(0, '.')

from app.services.cache_service import clear_cache
clear_cache()

print("=" * 70)
print("DATA VALIDATION & ANOMALY DETECTION TEST")
print("=" * 70)

from app.agents.scout import scout_agent

# Collect data with validation
print("\n[TEST] Collecting data for ITC.NS with validation...")
print("-" * 50)

result = scout_agent.collect_data("ITC.NS")

# Check currency correction
print("\n\n📊 CURRENCY VALIDATION")
print("-" * 50)
financials = result.get("financials", {})
print(f"Currency: {financials.get('currency')}")
print(f"Was Corrected: {financials.get('currency_corrected', False)}")
if financials.get('currency_corrected'):
    print(f"  Original: {financials.get('currency_original')}")
print(f"Market Cap: {financials.get('market_cap')}")

# Check anomalies
print("\n\n⚠️ ANOMALIES DETECTED")
print("-" * 50)
anomalies = result.get("anomalies", [])
if anomalies:
    for i, a in enumerate(anomalies, 1):
        print(f"\n{i}. [{a.get('severity', 'INFO')}] {a.get('type')}")
        print(f"   Message: {a.get('message')}")
        details = a.get("details", {})
        if details.get("requires_news_search"):
            print(f"   🔍 News search suggested: {details.get('suggested_query')}")
else:
    print("No anomalies detected.")

# Check news
print("\n\n📰 NEWS (Check for volatility-related)")
print("-" * 50)
news = result.get("news", [])
for i, n in enumerate(news[:5], 1):
    priority = n.get("priority", "")
    source = n.get("source", "Unknown")
    title = n.get("title", "")[:55]
    
    if priority == "HIGH":
        print(f"   ⚠️ [{source}] {title}...")
    else:
        print(f"   {i}. [{source}] {title}...")
    
    if n.get("reason"):
        print(f"      Reason: {n.get('reason')}")

# Data quality
print("\n\n✅ DATA QUALITY")
print("-" * 50)
quality = result.get("data_quality", {})
print(f"Overall: {quality.get('overall')}")
print(f"Components: {quality.get('components')}")
if quality.get("issues"):
    print(f"Issues: {quality.get('issues')}")

# Save full result
with open("data_validation_test_results.json", 'w') as f:
    # Remove history to keep file small
    result_copy = result.copy()
    if "technicals" in result_copy and "history" in result_copy["technicals"]:
        result_copy["technicals"]["history"] = result_copy["technicals"]["history"][-5:]
    json.dump(result_copy, f, indent=2, default=str)

print("\n\n✅ Results saved to data_validation_test_results.json")
