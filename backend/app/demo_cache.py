DEMO_ANALYSES = {
    "ASIANPAINTS.NS": {
        "orchestration_id": "demo_asianpaints",
        "asset_id": "ASIANPAINTS.NS",
        "match_score": 75,
        "match_result": {
            "score": 75,
            "recommendation": "HOLD",
            "action_if_owned": "HOLD - Quality business but premium valuation",
            "action_if_not_owned": "WAIT - Look for better entry points below 2800",
            "fit_reasons": [
                "Market leader in decorative paints with 50%+ market share",
                "Strong brand moat and distribution network",
                "Consistent dividend payer with 1.2% yield",
                "Expanding into adjacent categories"
            ],
            "concern_reasons": [
                "Premium valuation at 65x P/E",
                "Raw material cost volatility (crude, titanium dioxide)",
                "Increasing competition from Grasim/Birla Opus"
            ],
            "summary": "Asian Paints is India's premier decorative paints company with excellent fundamentals but trades at premium valuations. Best suited for long-term investors.",
            "breakdown": {
                "fundamental": 78,
                "macro": 72,
                "philosophy": 85,
                "risk": 70,
                "dna_match": 75
            }
        },
        "coach_verdict": {
            "verdict": "HOLD",
            "confidence": 75,
            "summary": "Asian Paints is a quality compounder with strong brand and distribution moat. However, current valuations leave limited upside. Consider accumulating on corrections below 2800."
        },
        "results": {
            "quant": {
                "score": 78,
                "analysis": "Asian Paints has ROE of 25%, operating margins of 18%, and revenue growth of 10% YoY. P/E of 65x is expensive vs historical average of 55x. Balance sheet is strong with minimal debt.",
                "confidence": 80,
                "sentiment": "neutral",
                "output": {
                    "pe_ratio": 65.0,
                    "roe": 0.25,
                    "debt_to_equity": 0.15,
                    "profit_margins": 0.18
                }
            },
            "macro": {
                "score": 72,
                "trend": "neutral",
                "analysis": "Paint sector benefits from housing recovery and renovation demand. However, crude oil volatility affects raw material costs. RBI rate cuts could boost housing demand.",
                "confidence": 75,
                "sentiment": "neutral"
            },
            "philosopher": {
                "score": 85,
                "alignment_score": 85,
                "analysis": "Asian Paints has an exceptional business moat built over 80+ years. Strong governance, family-professional management balance, and consistent capital allocation. ESG practices are improving with water recycling initiatives.",
                "confidence": 85,
                "sentiment": "positive",
                "output": {
                    "alignment": "High",
                    "ethical_strengths": ["Strong governance", "Community initiatives"],
                    "ethical_concerns": ["Chemical industry environmental impact"]
                }
            },
            "regret": {
                "score": 70,
                "risk_level": "MEDIUM",
                "analysis": "Key risks include raw material cost spikes (crude, TiO2), new competition from Grasim's Birla Opus, and rural demand slowdown. Downside of 25-30% possible in adverse scenario.",
                "confidence": 75,
                "sentiment": "neutral",
                "output": {
                    "risk_level": "Medium",
                    "max_drawdown_estimate": "25-30%",
                    "scenarios": ["Raw material cost spike", "Competition from Birla Opus"]
                }
            }
        },
        "market_data": {
            "price": 2450.00,
            "change": -0.85,
            "volume": 1250000,
            "high52w": 3422.00,
            "low52w": 2379.00,
            "pe_ratio": 65.0,
            "market_cap": "2.35T",
            "currency": "INR",
            "history": [
                {"date": "2026-01-06", "price": 2480.50},
                {"date": "2026-01-07", "price": 2465.25},
                {"date": "2026-01-08", "price": 2472.00},
                {"date": "2026-01-09", "price": 2458.75},
                {"date": "2026-01-10", "price": 2450.00}
            ]
        }
    },
    "TCS.NS": {
        "orchestration_id": "demo_tcs",
        "asset_id": "TCS.NS",
        "match_score": 87,
        "match_result": {
            "score": 87,
            "recommendation": "STRONG BUY",
            "action_if_owned": "HOLD - Strong fundamentals justify position",
            "action_if_not_owned": "BUY - Quality IT stock with consistent growth",
            "fit_reasons": [
                "Strong revenue growth of 8.2% YoY",
                "Consistent dividend payer - 3.1% yield",
                "Low debt-to-equity ratio of 0.05",
                "Global IT services leader with diversified client base"
            ],
            "concern_reasons": [
                "Premium valuation at 28x P/E",
                "Currency headwinds may impact margins"
            ],
            "summary": "TCS represents a high-quality, defensive IT investment with strong fundamentals and consistent shareholder returns.",
            "breakdown": {
                "fundamental": 88,
                "macro": 82,
                "philosophy": 90,
                "risk": 85,
                "dna_match": 89
            }
        },
        "coach_verdict": {
            "verdict": "BUY",
            "confidence": 87,
            "summary": "TCS is a core holding for any long-term portfolio. Strong fundamentals, excellent management, and consistent execution make this a low-risk, high-quality investment."
        },
        "results": {
            "quant": {
                "score": 88,
                "analysis": "TCS shows strong fundamentals with ROE of 45%, operating margins of 25%, and free cash flow yield of 3.2%. Revenue growth remains steady at 8.2% with improving margins.",
                "sentiment": "positive"
            },
            "macro": {
                "trend": "bullish",
                "analysis": "IT sector benefits from digital transformation spending. US tech budgets remain strong despite rate concerns. INR weakness provides tailwind for rupee earnings.",
                "sentiment": "positive"
            },
            "philosopher": {
                "alignment_score": 90,
                "analysis": "TCS has strong economic moat through scale, client relationships, and domain expertise. Management maintains conservative capital allocation with consistent dividend policy.",
                "sentiment": "positive"
            },
            "regret": {
                "risk_level": "LOW",
                "analysis": "Downside limited to 15-20% in adverse scenario. Strong balance sheet and cash generation provide buffer. Main risk is valuation compression in risk-off environment.",
                "sentiment": "neutral"
            }
        },
        "market_data": {
            "price": 4125.50,
            "change": 1.32,
            "volume": 2450000,
            "high52w": 4450.00,
            "low52w": 3180.00,
            "pe_ratio": 28.5,
            "market_cap": "15.2T",
            "currency": "INR"
        }
    },
    "RELIANCE.NS": {
        "orchestration_id": "demo_reliance",
        "asset_id": "RELIANCE.NS",
        "match_score": 72,
        "match_result": {
            "score": 72,
            "recommendation": "HOLD",
            "action_if_owned": "HOLD - Diversified business provides stability",
            "action_if_not_owned": "WAIT - Better entry points possible",
            "fit_reasons": [
                "Diversified conglomerate with multiple growth engines",
                "Jio and Retail segments showing strong growth",
                "Net debt reduction improving balance sheet"
            ],
            "concern_reasons": [
                "O2C segment facing margin pressure",
                "High capex needs for new energy transition",
                "Complex holding structure reduces transparency"
            ],
            "summary": "Reliance is a quality conglomerate but current valuations price in near-term growth. Better for patient, long-term investors.",
            "breakdown": {
                "fundamental": 75,
                "macro": 70,
                "philosophy": 68,
                "risk": 72,
                "dna_match": 74
            }
        },
        "coach_verdict": {
            "verdict": "HOLD",
            "confidence": 72,
            "summary": "Reliance offers diversified exposure to India's growth story. While fundamentals are solid, valuations are fair. Suitable as a core holding but not for aggressive accumulation at current levels."
        },
        "results": {
            "quant": {
                "score": 75,
                "analysis": "ROE of 8.5% is below peers but improving. Operating margins vary by segment - Jio at 50%, Retail at 8%, O2C at 6%. Revenue growth at 12% driven by consumer segments.",
                "sentiment": "neutral"
            },
            "macro": {
                "trend": "neutral",
                "analysis": "Mixed macro outlook. Telecom benefits from ARPU expansion. Retail gains from consumption. O2C faces global refining margin pressure. New energy investments are long-term bets.",
                "sentiment": "neutral"
            },
            "philosopher": {
                "alignment_score": 68,
                "analysis": "Execution track record is strong but capital allocation has become complex. Related party transactions and promoter pledging warrant monitoring. ESG transition is positive.",
                "sentiment": "neutral"
            },
            "regret": {
                "risk_level": "MEDIUM",
                "analysis": "Downside of 25-30% possible in market stress. O2C segment vulnerability to commodity cycles. Execution risk in new energy investments. Jio IPO timing uncertainty.",
                "sentiment": "neutral"
            }
        },
        "market_data": {
            "price": 2890.75,
            "change": -0.25,
            "volume": 5200000,
            "high52w": 3025.00,
            "low52w": 2220.00,
            "pe_ratio": 26.2,
            "market_cap": "19.6T",
            "currency": "INR"
        }
    },
    "INFY.NS": {
        "orchestration_id": "demo_infy",
        "asset_id": "INFY.NS",
        "match_score": 82,
        "match_result": {
            "score": 82,
            "recommendation": "BUY",
            "action_if_owned": "HOLD - Quality position to maintain",
            "action_if_not_owned": "BUY - Attractive valuation vs peers",
            "fit_reasons": [
                "Best-in-class margins at 21% operating",
                "Strong deal wins and pipeline",
                "Attractive dividend yield of 2.8%",
                "Lower valuation than TCS offers better risk-reward"
            ],
            "concern_reasons": [
                "Attrition rates elevated at 15%",
                "Large deal execution risk"
            ],
            "summary": "Infosys offers compelling value in IT services with strong execution and improving growth outlook.",
            "breakdown": {
                "fundamental": 84,
                "macro": 80,
                "philosophy": 82,
                "risk": 80,
                "dna_match": 84
            }
        },
        "coach_verdict": {
            "verdict": "BUY",
            "confidence": 82,
            "summary": "Infosys is a quality IT services company trading at reasonable valuations. Strong fundamentals, consistent capital returns, and improving growth make it attractive for long-term investors."
        },
        "results": {
            "quant": {
                "score": 84,
                "analysis": "ROE of 31%, operating margins of 21.5%, FCF yield of 3.8%. Revenue growth guidance of 4-7% is conservative. Large deal TCV improving.",
                "sentiment": "positive"
            },
            "macro": {
                "trend": "bullish",
                "analysis": "IT spending resilient. Cloud migration and AI services driving demand. US banking weakness offset by manufacturing and retail strength.",
                "sentiment": "positive"
            },
            "philosopher": {
                "alignment_score": 82,
                "analysis": "Strong governance under Nilekani. ESG leadership in Indian IT. Capital allocation is shareholder friendly with buybacks and dividends.",
                "sentiment": "positive"
            },
            "regret": {
                "risk_level": "LOW",
                "analysis": "Downside limited to 15-18%. Strong balance sheet with net cash. Main risk is guidance miss or client concentration events.",
                "sentiment": "neutral"
            }
        },
        "market_data": {
            "price": 1845.25,
            "change": 0.85,
            "volume": 4100000,
            "high52w": 1980.00,
            "low52w": 1355.00,
            "pe_ratio": 24.8,
            "market_cap": "7.7T",
            "currency": "INR"
        }
    },
    "HDFCBANK.NS": {
        "orchestration_id": "demo_hdfc",
        "asset_id": "HDFCBANK.NS",
        "match_score": 78,
        "match_result": {
            "score": 78,
            "recommendation": "BUY",
            "action_if_owned": "HOLD - Core banking position",
            "action_if_not_owned": "BUY - Best private bank at attractive valuation",
            "fit_reasons": [
                "Market leader in private banking",
                "Best-in-class asset quality with 1.2% GNPA",
                "Post-merger synergies to drive growth",
                "Trading below historical valuation"
            ],
            "concern_reasons": [
                "Merger integration still ongoing",
                "NIM pressure from deposit competition",
                "Large size limits growth rate"
            ],
            "summary": "HDFC Bank remains India's premier private bank. Post-merger, it offers compelling value at current valuations.",
            "breakdown": {
                "fundamental": 82,
                "macro": 75,
                "philosophy": 80,
                "risk": 76,
                "dna_match": 78
            }
        },
        "coach_verdict": {
            "verdict": "BUY",
            "confidence": 78,
            "summary": "HDFC Bank is a compounding machine trading at attractive valuations post-merger. Best risk-adjusted way to play India's financialization theme."
        },
        "results": {
            "quant": {
                "score": 82,
                "analysis": "ROE of 16.5% (improving post-merger). NIM at 3.5%. Loan growth of 15%+. Cost-to-income ratio improving to 40%. Asset quality remains pristine.",
                "sentiment": "positive"
            },
            "macro": {
                "trend": "bullish",
                "analysis": "Credit growth environment supportive. Rate cycle peak provides NIM stability. Housing finance integration adds mortgage growth runway.",
                "sentiment": "positive"
            },
            "philosopher": {
                "alignment_score": 80,
                "analysis": "Gold standard in Indian banking governance. Conservative underwriting culture maintained. Management succession well handled.",
                "sentiment": "positive"
            },
            "regret": {
                "risk_level": "LOW",
                "analysis": "Downside limited to 20% in stress. Strong capital buffers. Main risk is merger integration delays or deposit market share loss.",
                "sentiment": "neutral"
            }
        },
        "market_data": {
            "price": 1725.50,
            "change": 0.32,
            "volume": 8500000,
            "high52w": 1795.00,
            "low52w": 1420.00,
            "pe_ratio": 19.2,
            "market_cap": "13.1T",
            "currency": "INR"
        }
    }
}

def get_demo_analysis(ticker: str):
    normalized = ticker.upper()
    if not normalized.endswith('.NS'):
        normalized = f"{normalized}.NS"
    return DEMO_ANALYSES.get(normalized)

def is_demo_ticker(ticker: str) -> bool:
    normalized = ticker.upper()
    if not normalized.endswith('.NS'):
        normalized = f"{normalized}.NS"
    return normalized in DEMO_ANALYSES
