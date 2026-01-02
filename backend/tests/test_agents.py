"""
Test script to verify agent improvements and output format.
"""
import json
import sys
sys.path.insert(0, '.')

# Import all agents
from app.agents.quant import quant_agent
from app.agents.macro import macro_agent
from app.agents.philosopher import philosopher_agent
from app.agents.regret import regret_agent
from app.agents.coach import coach_agent

print("=" * 60)
print("AGENT IMPROVEMENT VERIFICATION TEST")
print("=" * 60)

# Sample context data for testing
sample_financial_context = [
    {
        "content": {
            "symbol": "TCS.NS",
            "pe_ratio": 28.5,
            "forward_pe": 24.0,
            "peg_ratio": 1.8,
            "profit_margins": 0.22,
            "return_on_equity": 0.48,
            "debt_to_equity": 8.5,
            "market_cap": "14.5T",
            "sector": "Technology"
        },
        "metadata": {"type": "financials"}
    }
]

sample_macro_context = [
    {
        "content": {
            "volatility_index": 18.5,
            "interest_rate_proxy": 4.2,
            "market_change_pct": 0.5
        },
        "metadata": {"type": "macro"}
    }
]

sample_full_context = sample_financial_context + sample_macro_context


def test_agent(agent, context, name):
    """Test an agent and verify output format."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print("=" * 60)
    
    try:
        result = agent.run(context)
        
        # Check for required fields in new format
        required_fields = ["agent", "timestamp", "output", "confidence", "data_quality", "fallback_used", "analysis"]
        missing = [f for f in required_fields if f not in result]
        
        if missing:
            print(f"❌ Missing fields: {missing}")
        else:
            print(f"✅ All required fields present")
        
        print(f"   Agent: {result.get('agent')}")
        print(f"   Confidence: {result.get('confidence')}")
        print(f"   Data Quality: {result.get('data_quality')}")
        print(f"   Fallback Used: {result.get('fallback_used')}")
        print(f"   Output Keys: {list(result.get('output', {}).keys())}")
        
        # Print formatted output
        print(f"\n   Full Output:")
        print(json.dumps(result, indent=2, default=str)[:1000] + "...")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


# Run tests
results = []

results.append(("Quant Agent", test_agent(quant_agent, sample_financial_context, "Quant Agent")))
results.append(("Macro Agent", test_agent(macro_agent, sample_macro_context, "Macro Agent")))
results.append(("Philosopher Agent", test_agent(philosopher_agent, sample_full_context, "Philosopher Agent")))
results.append(("Regret Agent", test_agent(regret_agent, sample_full_context, "Regret Agent")))
results.append(("Coach Agent", test_agent(coach_agent, sample_full_context, "Coach Agent")))

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
for name, passed in results:
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {name}: {status}")

all_passed = all(p for _, p in results)
print(f"\nOverall: {'✅ All tests passed!' if all_passed else '❌ Some tests failed'}")
