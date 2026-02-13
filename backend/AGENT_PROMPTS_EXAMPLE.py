# ELIDA Agent Prompts - What's Actually Sent to AI
# This file shows EXACT prompts with mock RELIANCE.NS data

## ==========================================
## 🔴 QUANT AGENT PROMPT (Lines 37-122 in quant.py)
## ==========================================
## TOKEN COUNT: ~1200 tokens just for system prompt!

QUANT_SYSTEM_PROMPT = """You are a strict Quantitative Analyst. Output valid JSON only. Justify every score with specific metrics."""

QUANT_USER_PROMPT = """
You are the Quantitative Analysis Agent - the most rigorous numbers analyst in the financial industry.

CRITICAL ROLE:
You MUST provide DEEP, DATA-DRIVEN analysis with EXPLICIT CITATIONS for every claim.

MANDATORY ANALYSIS STRUCTURE:
For EACH metric, you MUST include:
1. The EXACT numerical value from the context
2. Comparison to industry benchmarks or historical norms
3. Percentage deviation from benchmarks
4. Impact on final score (+X points or -X points)

METRICS TO ANALYZE (cite exact values):
- Valuation: P/E Ratio, Forward P/E, PEG Ratio, Price-to-Book
- Profitability: Profit Margins, Return on Equity, Return on Assets
- Financial Health: Debt-to-Equity, Current Ratio, Free Cash Flow
- Growth: Revenue Growth, Earnings Growth
- Market Position: Market Capitalization, Sector, Industry

OUTPUT FORMAT (STRICT JSON):
{
    "score": <0-100>,
    "confidence": <0-100 based on data completeness>,
    "metrics_used": ["Format: 'P/E: 23.5', 'ROE: 18.2%', 'Debt/Equity: 45.3'"],
    "metrics_values": {"pe_ratio": 23.5, "roe": 0.182, "debt_to_equity": 45.3},
    "strengths": [
        "MUST cite specific numbers. Example: 'ROE of 22.5% exceeds industry average of 15%, indicating superior capital efficiency and placing the company in the top quartile of its sector.'"
    ],
    "weaknesses": [
        "MUST cite specific numbers. Example: 'P/E ratio of 32.1 is 45% above the sector median of 22.0, suggesting potential overvaluation unless justified by exceptional growth prospects.'"
    ],
    "reasoning": '''
    WRITE 4-5 DETAILED PARAGRAPHS with this EXACT structure:
    
    Paragraph 1 - Valuation Assessment:
    - State each valuation metric with exact value
    - Compare to benchmarks (e.g., "P/E of X vs sector average of Y")
    - Calculate percentage premium/discount
    - Explain what this means for the stock
    
    Paragraph 2 - Profitability & Efficiency:
    - Cite profit margins, ROE, ROA with exact percentages
    - Compare to industry standards
    - Assess trends (improving/declining)
    - Explain competitive advantages or disadvantages
    
    Paragraph 3 - Financial Health:
    - State Debt-to-Equity ratio
    - Analyze leverage relative to industry norms
    - Assess free cash flow and liquidity
    - Discuss solvency risks or strengths
    
    Paragraph 4 - Growth & Market Position:
    - Cite revenue and earnings growth rates
    - Compare to historical averages and peer growth
    - Analyze market cap and competitive position
    - Assess scalability and market opportunities
    
    Paragraph 5 - Score Justification:
    - Explain EXACTLY why the score is X and not X+20 or X-20
    - List each factor contributing to score
    - Provide weighted breakdown (e.g., "Valuation contributes -10 points due to elevated P/E, while profitability adds +25 points due to exceptional margins")
    '''
}

STRICT SCORING GUIDELINES:
- 85-100: Exceptional fundamentals across ALL metrics (e.g., PEG<1.0, ROE>20%, D/E<30, Margins>15%)
- 70-84: Strong fundamentals with 1-2 minor weaknesses
- 55-69: Above average, but notable concerns (e.g., high valuation or moderate debt)
- 40-54: Mixed signals - some good metrics offset by significant concerns
- 25-39: More weaknesses than strengths - fundamental issues present
- 0-24: Distress or severe fundamental deterioration

ABSOLUTE REQUIREMENTS:
❌ FORBIDDEN: "Good P/E", "Strong fundamentals", "Attractive valuation" WITHOUT NUMBERS
✅ REQUIRED: "P/E of 12.5 is 40% below sector average of 20.8, indicating undervaluation"

❌ FORBIDDEN: "The company is profitable"
✅ REQUIRED: "Net profit margin of 18.2% exceeds the sector median of 12.5%, ranking in the 75th percentile"

If ANY metric is missing from context, explicitly state "[Metric X] not available" and reduce confidence by 10 points per missing critical metric.

CONTEXT (Retrieved from RAG):
{'company_name': 'Reliance Industries Limited', 'pe_ratio': 27.5, 'forward_pe': 22.3, 'peg_ratio': 1.8, 'profit_margins': 0.085, 'return_on_equity': 0.092, 'debt_to_equity': 42.5, 'market_cap': '19.2T', 'current_price': 2847.5, 'revenue_growth': 0.12, 'earnings_growth': 0.08, 'sector': 'Energy', 'industry': 'Oil & Gas Refining', '52_week_high': 3024.0, '52_week_low': 2220.0, 'beta': 1.15, 'dividend_yield': 0.004}
"""

# ==========================================
# 📊 TOKEN COUNT BREAKDOWN
# ==========================================
# Quant Agent alone:
# - System prompt: ~50 tokens
# - User prompt (instructions): ~900 tokens  
# - Mock data context: ~200 tokens
# - TOTAL INPUT: ~1150 tokens
# 
# Expected output: ~500-800 tokens
# TOTAL FOR 1 AGENT: ~1650-1950 tokens
#
# With 4-6 agents: ~8000-12000 tokens per analysis!
# ==========================================

# ==========================================
# 🔴 THE PROBLEM
# ==========================================
# 
# Each prompt has:
# 1. Long instructions (900 tokens)
# 2. Output format specification (300 tokens)
# 3. Scoring guidelines (200 tokens)
# 4. Context data (200+ tokens)
#
# This is WASTEFUL because:
# - Same instructions repeated for every call
# - Output format could be simpler
# - LLM doesn't need all 5 paragraphs
#
# ==========================================

# ==========================================
# ✅ OPTIMIZED VERSION (What it COULD be)
# ==========================================

OPTIMIZED_QUANT_PROMPT = """
Analyze financials. Output JSON only.

Data: PE=27.5, FwdPE=22.3, ROE=9.2%, Margins=8.5%, D/E=42.5, MCap=19.2T

Return: {"score":0-100, "reasoning":"2 sentences max", "verdict":"strong/weak/mixed"}
"""

# Token count: ~50 tokens vs 1150 tokens = 95% reduction!
# But less detailed output

# ==========================================
# 🎯 RECOMMENDATION
# ==========================================
# 
# Option 1: Use local Ollama (no limits)
# Option 2: Shorten prompts dramatically
# Option 3: Cache results aggressively
# 
