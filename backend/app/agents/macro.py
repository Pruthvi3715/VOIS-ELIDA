from typing import Any, Dict, List
from app.agents.base import BaseAgent


class MacroAgent(BaseAgent):
    """
    Global Macroeconomic Analysis Agent - Determines market environment.
    Enhanced with multiple indicators, confidence scoring, and structured output.
    """
    
    def __init__(self):
        super().__init__(name="Macro Agent")
        
        # Indicator thresholds
        self.thresholds = {
            "vix": {"low": 15, "high": 25},
            "interest_rate": {"low": 3.0, "high": 4.5},
            "rsi": {"oversold": 30, "overbought": 70}
        }

    def run(self, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze macroeconomic indicators and determine market trend.
        """
        # Filter for macro data
        macro_data = [c for c in context if c.get("metadata", {}).get("type") == "macro"]
        
        # Calculate data quality
        data_quality = self.calculate_data_quality(macro_data)
        
        # Prepare context
        context_str = "\n".join([str(c.get("content")) for c in macro_data])
        
        prompt = f"""
        You are the Global Macroeconomic Analysis Agent.

        ROLE:
        Provide a DETAILED analysis of the market environment. Don't just list indicators; explain their INTERCONNECTION and IMPACT.

        INDICATORS TO ANALYZE:
        - VIX: Cite specific level (e.g., 14.5). Explain if it implies complacency or fear.
        - Rates (10Y Yield): Cite specific %. Explain impact on discount rates/valuations.
        - Market Indices: Trend direction and strength.
        - Currency/GDP: Broader economic context.

        OUTPUT FORMAT (STRICT JSON):
        {{
            "trend": "<Bullish|Bearish|Neutral>",
            "confidence": <0-100>,
            "indicators_analyzed": [
                {{"name": "indicator", "value": "EXACT VALUE", "signal": "positive/negative/neutral", "impact": "Detailed explanation of impact"}}
            ],
            "macro_risks": ["Detailed sentence describing specific risk"],
            "macro_tailwinds": ["Detailed sentence describing positive factor"],
            "reasoning": "DETAILED SYNTHESIS: Write 3 paragraphs. 1) Current Regime (e.g., High-Rate/Low-Vol). 2) Impact on this asset class. 3) Forward outlook. CITE ALL VALUES."
        }}

        RULES:
        1. QUANTIFY EVERYTHING. Don't say "High VIX", say "VIX at 28.5 indicates extreme fear".
        2. CONNECT THE DOTS. How do high rates affect THIS asset's valuation?
        3. NO VAGUE STATEMENTS. "Market is good" is forbidden.

        CONTEXT (Retrieved from RAG):
        {context_str if context_str else "No macro data available in context."}
        """
        
        response = self.call_llm(
            prompt=prompt,
            system_prompt="You are a Macro Strategist. Output valid JSON. Be precise about indicators.",
            fallback_func=self._rule_based_macro,
            fallback_args=macro_data
        )
        
        # Parse response
        parsed = self._parse_response(response, macro_data)
        
        # Determine if fallback was used
        fallback_used = "[Fallback]" in response or "[Rule-Based]" in response
        
        # Adjust confidence based on data quality
        if data_quality == "Low":
            parsed["confidence"] = min(parsed["confidence"], 40)
            if parsed["trend"] != "Neutral":
                parsed["trend"] = "Neutral"  # Force neutral on low data
        
        return self.format_output(
            output_data={
                "trend": parsed["trend"],
                "indicators_analyzed": parsed.get("indicators_analyzed", []),
                "macro_risks": parsed.get("macro_risks", []),
                "macro_tailwinds": parsed.get("macro_tailwinds", [])
            },
            confidence=parsed["confidence"],
            data_quality=data_quality,
            fallback_used=fallback_used,
            analysis=parsed.get("reasoning", response)
        )

    def _parse_response(self, response: str, macro_data: List[Dict]) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        """
        result = {
            "trend": "Neutral",
            "confidence": 50,
            "indicators_analyzed": [],
            "macro_risks": [],
            "macro_tailwinds": [],
            "reasoning": response
        }
        
        # Try JSON parsing
        parsed_json = self.parse_json_from_response(response)
        if parsed_json:
            result.update(parsed_json)
            # Validate trend
            valid_trends = ["Bullish", "Bearish", "Neutral"]
            if result["trend"] not in valid_trends:
                result["trend"] = self.extract_level(result["trend"], valid_trends, "Neutral")
            result["confidence"] = max(0, min(100, result.get("confidence", 50)))
            return result
        
        # Fallback extraction
        result["trend"] = self.extract_level(response, ["Neutral", "Bullish", "Bearish"], "Neutral")
        result["confidence"] = self.extract_confidence(response, 50)
        
        return result

    def _rule_based_macro(self, macro_data: List[Dict[str, Any]]) -> str:
        """
        Enhanced rule-based macro analysis with multiple indicators.
        """
        trend_score = 0  # Positive = bullish, Negative = bearish
        confidence = 30
        indicators_analyzed = []
        macro_risks = []
        macro_tailwinds = []
        
        for item in macro_data:
            content = item.get("content", "")
            try:
                import ast
                data = content if isinstance(content, dict) else ast.literal_eval(str(content))
                
                # VIX Analysis
                vix = data.get("volatility_index")
                if isinstance(vix, (int, float)):
                    indicators_analyzed.append({
                        "name": "VIX",
                        "value": vix,
                        "signal": "positive" if vix < 15 else ("negative" if vix > 25 else "neutral"),
                        "impact": f"VIX at {vix:.1f}"
                    })
                    
                    if vix > 25:
                        trend_score -= 2
                        macro_risks.append(f"Elevated fear (VIX: {vix:.1f})")
                    elif vix < 15:
                        trend_score += 2
                        macro_tailwinds.append(f"Low volatility environment (VIX: {vix:.1f})")
                    else:
                        trend_score += 0.5
                    
                    confidence += 15
                
                # Interest Rate / 10Y Yield Analysis
                rate = data.get("interest_rate_proxy")
                if isinstance(rate, (int, float)):
                    indicators_analyzed.append({
                        "name": "10Y Treasury Yield",
                        "value": rate,
                        "signal": "negative" if rate > 4.5 else ("positive" if rate < 3 else "neutral"),
                        "impact": f"Yield at {rate:.2f}%"
                    })
                    
                    if rate > 4.5:
                        trend_score -= 1.5
                        macro_risks.append(f"High yields ({rate:.2f}%) pressure equity valuations")
                    elif rate > 4.0:
                        trend_score -= 0.5
                    elif rate < 3.0:
                        trend_score += 1
                        macro_tailwinds.append(f"Supportive rate environment ({rate:.2f}%)")
                    
                    confidence += 15
                
                # Market Index Analysis
                market_change = data.get("market_change_pct")
                if isinstance(market_change, (int, float)):
                    indicators_analyzed.append({
                        "name": "Market Momentum",
                        "value": market_change,
                        "signal": "positive" if market_change > 0 else "negative",
                        "impact": f"Market {'+' if market_change > 0 else ''}{market_change:.2f}%"
                    })
                    
                    if market_change > 1:
                        trend_score += 1
                        macro_tailwinds.append(f"Positive market momentum ({market_change:+.2f}%)")
                    elif market_change < -1:
                        trend_score -= 1
                        macro_risks.append(f"Negative market momentum ({market_change:+.2f}%)")
                    
                    confidence += 10
                
            except Exception as e:
                continue
        
        # Determine trend
        if trend_score >= 2:
            trend = "Bullish"
        elif trend_score <= -2:
            trend = "Bearish"
        else:
            trend = "Neutral"
        
        # Cap confidence
        confidence = min(70, confidence)
        
        if not indicators_analyzed:
            return """[Rule-Based Fallback] No macro indicators found in RAG context.
Trend: Neutral
Confidence: 20
Reasoning: Unable to determine macro environment due to missing indicator data. Defaulting to neutral stance."""
        
        result = {
            "trend": trend,
            "confidence": confidence,
            "indicators_analyzed": indicators_analyzed,
            "macro_risks": macro_risks,
            "macro_tailwinds": macro_tailwinds,
            "reasoning": f"[Rule-Based Fallback] Analyzed {len(indicators_analyzed)} macro indicators. Net trend score: {trend_score:+.1f}."
        }
        
        import json
        return f"[Rule-Based Analysis]\n```json\n{json.dumps(result, indent=2)}\n```"


macro_agent = MacroAgent()
