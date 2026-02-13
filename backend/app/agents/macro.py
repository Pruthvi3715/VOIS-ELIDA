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
        Region-aware: Uses India indicators for .NS/.BO stocks, US for others.
        """
        # Filter for macro data
        macro_data = [c for c in context if c.get("metadata", {}).get("type") == "macro"]
        
        # Detect region from asset_id in context
        region = "US"  # Default
        for c in context:
            asset_id = c.get("metadata", {}).get("asset_id", "")
            if asset_id.upper().endswith((".NS", ".BO")):
                region = "INDIA"
                break
        
        # Calculate data quality
        data_quality = self.calculate_data_quality(macro_data)
        
        # Prepare context
        context_str = "\n".join([str(c.get("content")) for c in macro_data])
        
        # Region-specific prompt sections
        if region == "INDIA":
            indicators_section = """
        INDICATORS TO ANALYZE (INDIA FOCUS - THIS IS AN INDIAN STOCK):
        - India VIX: Cite specific level. Explain if it implies market fear or stability.
        - RBI Repo Rate: Current rate and impact on borrowing costs and valuations.
        - Nifty 50 / Sensex: Trend direction and strength of Indian market.
        - INR/USD Exchange Rate: Currency strength and FII flow implications.
        - Indian Inflation/GDP: Economic growth context.
        
        IMPORTANT: This is an INDIAN stock (.NS/.BO). Focus on INDIAN macro indicators.
        Do NOT focus primarily on US indicators like S&P 500 or US Treasury Yields.
        US markets can be mentioned as secondary context, but prioritize RBI policy, 
        Nifty trends, and Indian economic data."""
        else:
            indicators_section = """
        INDICATORS TO ANALYZE (US FOCUS):
        - VIX: Cite specific level (e.g., 14.5). Explain if it implies complacency or fear.
        - Rates (10Y Yield): Cite specific %. Explain impact on discount rates/valuations.
        - S&P 500 / Market Indices: Trend direction and strength.
        - DXY / Currency: Broader economic context.
        - Fed Policy: Rate expectations and impact."""
        
        prompt = f"""Analyze macro environment for {region} markets. Return JSON only.

REGION: {region}
DATA:
{context_str if context_str else "No macro data available"}

OUTPUT FORMAT:
{{
    "trend": "Bullish|Bearish|Neutral",
    "confidence": 0-100,
    "reasoning": "2-3 sentences citing specific indicator values (VIX, rates, etc.)",
    "macro_risks": ["1-2 specific risks"],
    "macro_tailwinds": ["1-2 positive factors"]
}}

For {region} stocks, focus on {"India VIX, RBI rates, Nifty trend" if region == "INDIA" else "VIX, Fed policy, S&P 500 trend"}."""
        
        response = self.call_llm(
            prompt=prompt,
            system_prompt=self.get_guardrail_system_prompt(f"You are a Macro Strategist specializing in {region} markets. Output valid JSON. Be precise about indicators. Only cite indicators that are present in the data."),
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
        
        # Derive numeric score from trend
        trend_scores = {"Bullish": 75, "Neutral": 50, "Bearish": 30}
        score = trend_scores.get(parsed["trend"], 50)
        # Adjust score based on confidence
        score = int(score * (0.7 + 0.3 * parsed["confidence"] / 100))
        
        return self.format_output(
            output_data={
                "score": score,
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
