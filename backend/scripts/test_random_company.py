import sys, os
sys.path.append(os.getcwd())
from dotenv import load_dotenv
load_dotenv(override=True)
from app.orchestrator import orchestrator
from app.models.investor_dna import InvestorDNA

# Test company: TSLA
asset_id = 'TSLA'
profile = InvestorDNA(user_id='test_output', risk_tolerance='moderate', investment_style='value')

print('='*60)
print(f'TESTING: {asset_id}')
print('='*60)

# Ingest
result = orchestrator.ingest_asset(asset_id)
print(f'Ingest: {result.get("status")}')

# Analyze
analysis = orchestrator.retrieve_context('analysis', asset_id, profile)

print()
print('='*60)
print('FULL AGENT OUTPUTS:')
print('='*60)

# Agent results are in the 'results' key
agent_results = analysis.get('results', {})

for agent_name in ['quant', 'macro', 'philosopher', 'regret']:
    print(f'\n{"="*20} {agent_name.upper()} AGENT {"="*20}')
    agent_data = agent_results.get(agent_name, {})
    
    # Print the full analysis text
    if 'analysis' in agent_data:
        print(f'ANALYSIS TEXT:')
        print(agent_data['analysis'][:800])
        if len(agent_data['analysis']) > 800:
            print('...[truncated]')
    
    # Print structured output
    if 'output' in agent_data:
        out = agent_data['output']
        print(f'\nSTRUCTURED OUTPUT:')
        print(f'  Score: {out.get("score", "N/A")}')
        print(f'  Trend: {out.get("trend", "N/A")}')
        print(f'  Alignment: {out.get("alignment", "N/A")}')
        print(f'  Risk Level: {out.get("risk_level", "N/A")}')
        print(f'  Strengths: {out.get("strengths", [])[:3]}')
        print(f'  Weaknesses: {out.get("weaknesses", [])[:3]}')
    
    # Print confidence
    print(f'  Confidence: {agent_data.get("confidence", "N/A")}')
    print(f'  Data Quality: {agent_data.get("data_quality", "N/A")}')

# Coach output
print(f'\n{"="*20} COACH SYNTHESIZER {"="*20}')
coach = analysis.get('coach_verdict', {})
if isinstance(coach, dict):
    print(f'VERDICT: {coach.get("verdict", "N/A")}')
    if 'analysis' in coach:
        print(f'SYNTHESIS:\n{coach["analysis"][:600]}...')
else:
    print(f'COACH OUTPUT:\n{str(coach)[:600]}')

# Match Score Breakdown
print()
print('='*60)
print('FINAL MATCH SCORE:')
print('='*60)
match = analysis.get('match_result', {})
print(f'Score: {match.get("score", "N/A")}%')
print(f'Recommendation: {match.get("recommendation", "N/A")}')
print(f'\nSCORE BREAKDOWN:')
breakdown = match.get('breakdown', {})
print(f'  Fundamental (Quant): {breakdown.get("fundamental", "N/A")}')
print(f'  Macro:               {breakdown.get("macro", "N/A")}')
print(f'  Philosophy:          {breakdown.get("philosophy", "N/A")}')
print(f'  Risk:                {breakdown.get("risk", "N/A")}')
print(f'  DNA Match:           {breakdown.get("dna_match", "N/A")}')
print(f'\nFit Reasons: {match.get("fit_reasons", [])}')
print(f'Concerns: {match.get("concern_reasons", [])}')
